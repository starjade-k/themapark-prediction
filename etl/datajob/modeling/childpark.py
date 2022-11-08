from datetime import date
import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import skew
from pyspark.sql.functions import col, lit
from datajob.modeling.navi_predict import NaviPredict
from datajob.modeling.sbw_out_predict import SbwOutPredict
from infra.spark_session import get_spark_session
from infra.jdbc import find_data, save_data, DataMart, DataWarehouse, OperationDB, overwrite_trunc_data
from infra.util import cal_std_day_after2
from xgboost import XGBRegressor


class ChildParkModeling:
    FILE_DIR = '/theme_park/final/'

    @classmethod
    def exec(cls):
        # ㅡㅡㅡㅡㅡㅡ train ㅡㅡㅡㅡㅡㅡ
        df = find_data(DataMart, "PRE_CHILDPARK")
        df = df.drop('PC_IDX', 'SBW_IN_NUM')
        df = df.toPandas()
        df = df.astype({'DAY': 'int32', 'HOLIDAY_OX': 'int32', 'ENT_NUM': 'int32', 'HIGH_TEMP': 'float',
                        'LOW_TEMP': 'float', 'RAIN_AMOUNT': 'float', 'AVG_WIND': 'float', 'HIGH_WIND': 'float',
                        'PM10': 'int32', 'PM25': 'int32', 'SBW_OUT_NUM': 'int32',
                        'EVENT_OX': 'int32', 'NAVI_SRC_NUM': 'int32', 'CORONA_PAT': 'int32',})
        
        df = cls.child_grand_park(df, test=False)
        y_train = df['ENT_NUM']
        X_train = df.drop(['ENT_NUM'], axis=1, inplace=False)
        
        # ㅡㅡㅡㅡㅡㅡㅡ testX 만들기 ㅡㅡㅡㅡㅡㅡㅡ

        # db에서 테마파크 번호 가져오기
        df_themepark = find_data(DataWarehouse, "THEMEPARK")
        childpark_num = df_themepark.where(col('THEME_NAME') == '서울어린이대공원').first()[0]

        # 미래 공휴일 정보
        df_hol = find_data(DataMart, 'PRE_HOLIDAY')
        df_hol = df_hol.select(col('STD_DATE'), col('HOLIDAY_OX')) \

        # 미래 날씨 정보
        df_weather = find_data(DataMart, 'PRE_AIR_WEATHER')
        df_weather = df_weather.select(col('STD_DATE'), col('HIGH_TEMP'), col('LOW_TEMP'), col('RAIN_AMOUNT'), col('AVG_WIND'), col('HIGH_WIND'), col('PM10'), col('PM25')) \
                                .where(col('THEME_NUM') == int(childpark_num)) \

        # 미래 행사 정보
        df_event = find_data(DataMart, 'PRE_THEMEPARK_EVENT')
        df_event = df_event.select(col('STD_DATE'), col('EVENT_OX')) \
                            .where(col('THEME_NUM') == int(childpark_num)) \

        # 요일정보
        dates = df_event.select(col('STD_DATE')).collect()
        dates_weekday = []
        for d in dates:
            tmp_dict = {}
            tmp_dict['STD_DATE'] = d['STD_DATE']
            tmp_dict['DAY'] = d['STD_DATE'].weekday() + 1
            dates_weekday.append(tmp_dict)
        df_weekday = get_spark_session().createDataFrame(dates_weekday)

        # 네비게이션 예측 정보
        df_navi = NaviPredict.exec('서울어린이대공원')

        # 지하철 하차 승객수 예측 정보
        df_sbwout = SbwOutPredict.exec('서울어린이대공원')
        
        df_test = df_hol.join(df_weather, on=['STD_DATE'])
        df_test = df_test.join(df_event, on=['STD_DATE'])
        df_test = df_test.join(df_weekday, on=['STD_DATE'])
        df_test = df_test.join(df_sbwout, on=['STD_DATE'])
        df_test = df_test.join(df_navi, on=['STD_DATE'])
        df_test = df_test.withColumn('CORONA_PAT', lit(0))
        df_test = df_test.withColumn('ENT_NUM', lit(0))

        df_test = df_test.toPandas()
        df_test = df_test.astype({'DAY': 'int32', 'HOLIDAY_OX': 'int32', 'ENT_NUM': 'int32', 'HIGH_TEMP': 'float',
                        'LOW_TEMP': 'float', 'RAIN_AMOUNT': 'float', 'AVG_WIND': 'float', 'HIGH_WIND': 'float',
                        'PM10': 'int32', 'PM25': 'int32', 'SBW_OUT_NUM': 'int32',
                        'EVENT_OX': 'int32', 'NAVI_SRC_NUM': 'int32', 'CORONA_PAT': 'int32'})
        
        df_test = cls.child_grand_park(df_test, test=True)


        X_test = df_test.drop(['ENT_NUM'], axis=1, inplace=False)
        y_test = df_test['ENT_NUM']

        X_train = X_train[['HOLIDAY_OX', 'HIGH_TEMP', 'LOW_TEMP', 'RAIN_AMOUNT', 'AVG_WIND', 'PM10', 'PM25', 'SBW_OUT_NUM', 'EVENT_OX', 'NAVI_SRC_NUM', 'CORONA_PAT', 'DAY_1', 'DAY_2', 'DAY_3', 'DAY_4', 'DAY_5', 'DAY_6', 'DAY_7']]
        X_test = X_test[['HOLIDAY_OX', 'HIGH_TEMP', 'LOW_TEMP', 'RAIN_AMOUNT', 'AVG_WIND', 'PM10', 'PM25', 'SBW_OUT_NUM', 'EVENT_OX', 'NAVI_SRC_NUM', 'CORONA_PAT', 'DAY_1', 'DAY_2', 'DAY_3', 'DAY_4', 'DAY_5', 'DAY_6', 'DAY_7']]


        # ㅡㅡㅡㅡㅡㅡ train 함수 실행 ㅡㅡㅡㅡㅡㅡ
        res_ent = cls.train_by_xgbm(X_train, y_train, X_test)
        print(res_ent)
        data = []
        for i in range(len(res_ent)):
            tmp_dict = {}
            tmp_dict['STD_DATE'] = cal_std_day_after2(i)
            tmp_dict['THEME_NAME'] = '서울어린이대공원'
            tmp_dict['ENT_NUM'] = int(res_ent[i])
            data.append(tmp_dict)

        # 운영 DB에 저장
        df_fin = get_spark_session().createDataFrame(data) \
                                    .select(col('STD_DATE').cast('date'), col('THEME_NAME'), col('ENT_NUM').cast('integer'))
        overwrite_trunc_data(OperationDB, df_fin, "PRE_ENTRANCE")



    # 전처리함수
    def child_grand_park(df, test):
        # 날짜 index화
        df = df.set_index('STD_DATE')
        
        # 하차총승객수 가중치 추가
        df['SBW_OUT_NUM'] = df['SBW_OUT_NUM'] * 1.11
        
        # 최대풍속 drop
        df.drop(['HIGH_WIND'], axis=1, inplace=True)
        
        # 타겟값 로그변환
        original_DailyTotal = df['ENT_NUM']
        df['ENT_NUM'] = np.log1p(df['ENT_NUM'])
        
        # 범주형 데이터 원핫인코딩
        df = pd.get_dummies(df, columns=['DAY'])
        
        if not test:
            # 타겟 값을 네비게이션 값과 비교해본 후 이상치 제거
            cond1 = df['NAVI_SRC_NUM'] < 1000
            cond2 = df['ENT_NUM'] < np.log1p(2)
            outlier_index = df[cond1 & cond2].index
            df.drop(outlier_index, axis=0, inplace=True)
        
        # 왜곡이 심한 컬럼에 로그학습
        features_index = ['PM10', 'PM25', 'RAIN_AMOUNT', 'AVG_WIND', 'LOW_TEMP',
                        'HIGH_TEMP', 'SBW_OUT_NUM', 'NAVI_SRC_NUM', 'CORONA_PAT']
        skew_features = df[features_index].apply(lambda x:skew(x))
        skew_features_top = skew_features[skew_features > 1]
        df[skew_features_top.index] = np.log1p(df[skew_features_top.index])
        
        return df


    def train_by_xgbm(X_train, y_train, X_test):
        xgbm_reg = XGBRegressor(n_jobs=-1, colsample_bytree=0.7, eta=0.1, learning_rate=0.1, max_depth=3, min_child_weight=5, 
                        n_estimators=600, scale_pos_weight=0.5, subsample=0.7)
        xgbm_reg.fit(X_train, y_train)
        y_test = xgbm_reg.predict(X_test)
        y_test = np.expm1(y_test)
        return y_test
