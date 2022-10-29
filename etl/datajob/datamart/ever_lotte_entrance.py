from pyspark.sql.functions import col
from infra.jdbc import DataMart, DataWarehouse, find_data, save_data
from infra.spark_session import get_spark_session

class LotteEverEntrance:
    @classmethod
    def save(cls):
        df_themepark = find_data(DataWarehouse, "THEMEPARK")
        df_themepark.show()

        # db에서 테마파크 번호 가져오기
        everland_num = df_themepark.where(col('THEME_NAME') == '에버랜드').first()[0]
        lotteworld_num = df_themepark.where(col('THEME_NAME') == '롯데월드').first()[0]

        # DW에서 입장객 정보 가져오기
        df_ent = find_data(DataWarehouse, "THEME_ENTRANCE2")

        # 에버랜드 입장객 정보
        df_ever = df_ent.select(col('STD_DATE'), col('ENT_NUM').alias('EVER_ENT')) \
                        .where(col('THEME_NUM') == int(everland_num)) \
                        .distinct().sort(col('STD_DATE'))

        # 날짜(월별)만 가져오기
        dates = [row['STD_DATE'] for row in df_ever.collect()]

        # 롯데월드 입장객 정보
        df_lotte = df_ent.select(col('STD_DATE'), col('ENT_NUM')) \
                        .where(col('THEME_NUM') == int(lotteworld_num)) \
                        .distinct().sort(col('STD_DATE'))
        lotte_rows = df_lotte.collect()
        lotte_data = []
        for date in dates:
            for row in lotte_rows:
                if row['STD_DATE'] == date:
                    lotte_data.append((date, int(row['ENT_NUM'])))
                    break
            else:
                lotte_data.append((date, 0))
        
        df_lotte = get_spark_session().createDataFrame(lotte_data, ['STD_DATE', 'LOTTE_ENT'])

        # 두 데이터프레임 조인
        df_fin = df_ever.join(df_lotte, on='STD_DATE').sort('STD_DATE')
        df_fin.show()

        save_data(DataMart, df_fin, 'LOTTE_EVER_ENTRANCE')
