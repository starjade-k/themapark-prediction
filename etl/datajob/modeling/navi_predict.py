from datetime import datetime
from keras.models import load_model
from pyspark.sql.functions import col
from infra.jdbc import find_data, DataWarehouse
from datajob.modeling.predict_util import rescaler, predict
from infra.spark_session import get_spark_session
from infra.util import cal_std_day2

class NaviPredict:

    @classmethod
    def exec(cls, theme_name):
        # db에서 테마파크 번호 가져오기
        df_themepark = find_data(DataWarehouse, "THEMEPARK")
        theme_num = df_themepark.where(col('THEME_NAME') == theme_name).first()[0]

        # 어린이대공원 네비게이션 데이터 가져오기
        df_navi = find_data(DataWarehouse, "NAVI_SEARCH")
        df_navi = df_navi.select(col('STD_DATE'), col('SRC_NUM')) \
                        .where(col('THEME_NUM') == int(theme_num)) \
                        .sort(col('STD_DATE').asc())

        df_navi = df_navi.toPandas() # 판다스 df로 변환
        df_navi = df_navi.astype({'SRC_NUM': 'int32'}) # 형변환
        
        # 모델 실행
        if theme_name == '서울대공원':
            model = load_model('./datajob/modeling/seoulgp_navi_model.h5')
        elif theme_name == '서울어린이대공원':
            model = load_model('./datajob/modeling/childrenpark_model.h5')
        elif theme_name == '에버랜드':
            model = load_model('./datajob/modeling/everland_model.h5')
        elif theme_name == '롯데월드':
            model = load_model('./datajob/modeling/lotteworld_model.h5')
        
        df_fin = predict(df_navi, 8, model, 'SRC_NUM', 'NAVI_SRC_NUM')
        df_fin = rescaler(df_navi, df_fin, 'SRC_NUM', 'NAVI_SRC_NUM')

        # 컬럼 수정
        df_fin = df_fin.reset_index()
        df_fin.rename(columns={'index': 'STD_DATE'}, inplace=True)

        # spark df로 생성
        df_fin = get_spark_session().createDataFrame(df_fin)
        
        # 현재날짜~7일후 데이터만 추출
        fin_list = df_fin.collect()
        today = cal_std_day2(0)
        today_datetime = datetime(int(today[:4]), int(today[4:6]), int(today[6:8]))
        after_7day = cal_std_day2(-6)
        after_7day_datetime = datetime(int(after_7day[:4]), int(after_7day[4:6]), int(after_7day[6:8]))
        fin_data = []
        for row in fin_list:
            if row['STD_DATE'] >= today_datetime and row['STD_DATE'] <= after_7day_datetime:
                fin_data.append(row)

        # 최종 데이터프레임 생성
        df_fin = get_spark_session().createDataFrame(fin_data)
        df_fin = df_fin.withColumn('NAVI_SRC_NUM', df_fin.NAVI_SRC_NUM.cast('int'))
        df_fin.show()
        print(df_fin.dtypes)

        return df_fin