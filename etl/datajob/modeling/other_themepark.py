from datetime import date
import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import skew
from pyspark.sql.functions import col, lit
from datajob.modeling.navi_predict import NaviPredict
from datajob.modeling.sbw_out_predict import SbwOutPredict
from infra.spark_session import get_spark_session
from infra.jdbc import find_data, save_data, DataMart, DataWarehouse, OperationDB
from infra.util import cal_std_day_after2
from lightgbm import LGBMRegressor


class OtherThemeParkModeling:
    FILE_DIR = '/theme_park/final/'

    @classmethod
    def exec(cls):
        # ㅡㅡㅡㅡㅡㅡ train ㅡㅡㅡㅡㅡㅡ
        df = find_data(DataMart, "PRE_SEOULPARK")
        df = df.drop('PS_IDX', 'SBW_IN_NUM')
        df = df.toPandas()
        df = df.astype({'DAY': 'int32', 'HOLIDAY_OX': 'int32', 'ENT_NUM': 'int32', 'HIGH_TEMP': 'float',
                        'LOW_TEMP': 'float', 'RAIN_AMOUNT': 'float', 'AVG_WIND': 'float', 'HIGH_WIND': 'float',
                        'PM10': 'int32', 'PM25': 'int32', 'SBW_OUT_NUM': 'int32',
                        'EVENT_OX': 'int32', 'NAVI_SRC_NUM': 'int32', 'CORONA_PAT': 'int32'})
        
        df = cls.seoul_grand_park(df, test=False)
        y_train = df['ENT_NUM']
        X_train = df.drop(['ENT_NUM'], axis=1, inplace=False)
        
        # ㅡㅡㅡㅡㅡㅡㅡ testX 만들기 ㅡㅡㅡㅡㅡㅡㅡ

        # db에서 테마파크 번호 가져오기
        df_themepark = find_data(DataWarehouse, "THEMEPARK")
        seoulpark_num = df_themepark.where(col('THEME_NAME') == '서울대공원').first()[0]

        # 미래 공휴일 정보
        df_hol = find_data(DataMart, 'PRE_HOLIDAY')
        df_hol = df_hol.select(col('STD_DATE'), col('HOLIDAY_OX')) \

        # 미래 날씨 정보
        df_weather = find_data(DataMart, 'PRE_AIR_WEATHER')
        df_weather = df_weather.select(col('STD_DATE'), col('HIGH_TEMP'), col('LOW_TEMP'), col('RAIN_AMOUNT'), col('AVG_WIND'), col('HIGH_WIND'), col('PM10'), col('PM25')) \
                                .where(col('THEME_NUM') == int(seoulpark_num)) \

        # 미래 행사 정보
        df_event = find_data(DataMart, 'PRE_THEMEPARK_EVENT')
        df_event = df_event.select(col('STD_DATE'), col('EVENT_OX')) \
                            .where(col('THEME_NUM') == int(seoulpark_num)) \

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
        df_seoulpark_navi = NaviPredict.exec('서울대공원')

        # 지하철 하차 승객수 예측 정보
        df_sbwout = SbwOutPredict.exec('서울대공원')
        
        df_test = df_hol.join(df_weather, on=['STD_DATE'])
        df_test = df_test.join(df_event, on=['STD_DATE'])
        df_test = df_test.join(df_weekday, on=['STD_DATE'])
        df_test = df_test.join(df_sbwout, on=['STD_DATE'])
        df_test = df_test.join(df_seoulpark_navi, on=['STD_DATE'])
        df_test = df_test.withColumn('CORONA_PAT', lit(0))
        df_test = df_test.withColumn('ENT_NUM', lit(0))

        df_test = df_test.toPandas()
        df_test = df_test.astype({'DAY': 'int32', 'HOLIDAY_OX': 'int32', 'ENT_NUM': 'int32', 'HIGH_TEMP': 'float',
                        'LOW_TEMP': 'float', 'RAIN_AMOUNT': 'float', 'AVG_WIND': 'float', 'HIGH_WIND': 'float',
                        'PM10': 'int32', 'PM25': 'int32', 'SBW_OUT_NUM': 'int32',
                        'EVENT_OX': 'int32', 'NAVI_SRC_NUM': 'int32', 'CORONA_PAT': 'int32'})
        
        df_test = cls.seoul_grand_park(df_test, test=True)

        X_test = df_test.drop(['ENT_NUM'], axis=1, inplace=False)
        y_test = df_test['ENT_NUM']

        X_train = X_train.sort_index()

        # 서울대공원 train 함수 실행
        seoulpark_res_ent = cls.train_by_lgbm(X_train, y_train, X_test)

        # 서울대공원 데이터프레임 생성
        seoulpark_data = []
        for i in range(len(seoulpark_res_ent)):
            tmp_dict = {}
            tmp_dict['STD_DATE'] = cal_std_day_after2(i)
            tmp_dict['THEME_NAME'] = '서울대공원'
            tmp_dict['ENT_NUM'] = int(seoulpark_res_ent[i])
            seoulpark_data.append(tmp_dict)

        # ㅡㅡㅡㅡㅡ 입장객 수 예측정보 DB 저장 ㅡㅡㅡㅡㅡ
        
        # 서울대공원 입장객 예측정보 운영 DB에 저장
        df_seoulpark_fin = get_spark_session().createDataFrame(seoulpark_data) \
                                    .select(col('STD_DATE').cast('date'), col('THEME_NAME'), col('ENT_NUM').cast('integer'))
        df_seoulpark_fin.show()
        save_data(OperationDB, df_seoulpark_fin, "PRE_ENTRANCE")

        # 롯데월드 입장객 예측정보 운영 DB에 저장
        df_lotte_fin = df_seoulpark_fin.withColumn('ENT_NUM', (col('ENT_NUM') / 83764 * 499730).cast('integer'))
        df_lotte_fin = df_lotte_fin.withColumn('THEME_NAME', lit('롯데월드'))
        df_lotte_fin.show()
        save_data(OperationDB, df_lotte_fin, "PRE_ENTRANCE")

        # 에버랜드 입장객 예측정보 운영 DB에 저장
        df_ever_fin = df_seoulpark_fin.withColumn('ENT_NUM', (col('ENT_NUM') / 83764 * 460780).cast('integer'))
        df_ever_fin = df_ever_fin.withColumn('THEME_NAME', lit('에버랜드'))
        df_ever_fin.show()
        save_data(OperationDB, df_ever_fin, "PRE_ENTRANCE")


        # ㅡㅡㅡㅡㅡ 네비게이션 예측정보 DB 저장 ㅡㅡㅡㅡㅡ

        # 서울대공원 네비게이션 예측정보 운영 DB에 저장
        df_seoulpark_navi = df_seoulpark_navi.withColumn('CONGESTION', (col('NAVI_SRC_NUM') / 6616 * 100).cast('integer'))
        df_seoulpark_navi = df_seoulpark_navi.withColumn('THEME_NAME', lit('서울대공원'))
        df_seoulpark_navi.show()
        save_data(OperationDB, df_seoulpark_navi, "PRE_NAVI")

        # 롯데월드 네비게이션 예측 정보 구하고, 운영 DB에 저장
        df_lotteworld_navi = NaviPredict.exec('롯데월드')
        df_lotteworld_navi = df_lotteworld_navi.withColumn('CONGESTION', (col('NAVI_SRC_NUM') / 3290 * 100).cast('integer'))
        df_lotteworld_navi = df_lotteworld_navi.withColumn('THEME_NAME', lit('롯데월드'))
        df_lotteworld_navi.show()
        save_data(OperationDB, df_lotteworld_navi, "PRE_NAVI")

        # 에버랜드 네비게이션 예측 정보 구하고, 운영 DB에 저장
        df_everland_navi = NaviPredict.exec('에버랜드')
        df_everland_navi = df_everland_navi.withColumn('CONGESTION', (col('NAVI_SRC_NUM') / 9844 * 100).cast('integer'))
        df_everland_navi = df_everland_navi.withColumn('THEME_NAME', lit('에버랜드'))
        df_everland_navi.show()
        save_data(OperationDB, df_everland_navi, "PRE_NAVI")



    # 전처리함수
    def seoul_grand_park(df, test):
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

    def train_by_lgbm(X_train, y_train, X_test):
        lgb_reg = LGBMRegressor(n_jobs=-1, colsample_bytree=0.8, eta=0.1,
                            learning_rate=0.1, max_depth=3, n_estimators=100, subsample=0.7)
        lgb_reg.fit(X_train, y_train)
        y_test = lgb_reg.predict(X_test)
        y_test = np.expm1(y_test)
        return y_test
