from datetime import datetime
from keras.models import load_model
from pyspark.sql.functions import col
from infra.jdbc import find_data, DataWarehouse
from datajob.modeling.predict_util import rescaler, predict
from infra.spark_session import get_spark_session
from infra.util import cal_std_day2

class SbwOutPredict:

    @classmethod
    def exec(cls, theme_name):
        # db에서 테마파크 번호 가져오기
        df_themepark = find_data(DataWarehouse, "THEMEPARK")
        theme_num = df_themepark.where(col('THEME_NAME') == theme_name).first()[0]

        # 어린이대공원 네비게이션 데이터 가져오기
        df_sbw = find_data(DataWarehouse, "SUBWAY_INOUT")
        df_sbw = df_sbw.select(col('STD_DATE'), col('OUT_NUM')) \
                        .where(col('THEME_NUM') == int(theme_num)) \
                        .sort(col('STD_DATE').asc())

        df_sbw = df_sbw.toPandas()
        df_sbw = df_sbw.astype({'OUT_NUM': 'int32'})

        # 모델 실행
        model = load_model('./datajob/modeling/seoulgp_model.h5')
        df_fin = predict(df_sbw, 10, model, 'OUT_NUM', 'SBW_OUT_NUM')
        df_fin = rescaler(df_sbw, df_fin, 'OUT_NUM', 'SBW_OUT_NUM')

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
        df_fin = df_fin.withColumn('SBW_OUT_NUM', df_fin.SBW_OUT_NUM.cast('int'))
        df_fin.show()
        print(df_fin.dtypes)

        return df_fin