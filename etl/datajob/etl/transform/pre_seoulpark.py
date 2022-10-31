import datetime as dt
from pyspark.sql.functions import col, to_date
from infra.jdbc import find_data, DataWarehouse, DataMart, overwrite_trunc_data
from infra.spark_session import get_spark_session

class PreSeoulParkTransformer:
    @classmethod
    def transform(cls):
        df_themepark = find_data(DataWarehouse, "THEMEPARK")

        # db에서 테마파크 번호 가져오기
        childpark_num = df_themepark.where(col('THEME_NAME') == '서울어린이대공원').first()[0]
        seoulpark_num = df_themepark.where(col('THEME_NAME') == '서울대공원').first()[0]

        # 입장객수 데이터 가져오기
        df_ent = find_data(DataWarehouse, "THEME_ENTRANCE1")
        df_ent = df_ent.select(col('STD_DATE'), col('ENT_NUM')) \
                                .where(col('THEME_NUM') == int(seoulpark_num)) \
                                .where(col('STD_DATE') <= dt.datetime(2022, 6, 30)) \
                                .sort(col('STD_DATE').desc())

        # 날씨 데이터 가져오기
        df_weather = find_data(DataWarehouse, "DAILY_WEATHER")
        df_weather = df_weather.select(col('STD_DATE'), col('HIGH_TEMP'), col('LOW_TEMP'), col('RAIN_AMOUNT'), col('AVG_WIND'), col('HIGH_WIND')) \
                                .where(col('THEME_NUM') == int(seoulpark_num)) \
                                .where(col('STD_DATE') <= dt.datetime(2022, 6, 30)) \
                                .sort(col('STD_DATE').desc())

        # 미세먼지 데이터 가져오기
        df_air = find_data(DataWarehouse, "DAILY_AIR")
        df_air = df_air.select(col('STD_DATE'), col('PM10'), col('PM25')) \
                        .where(col('THEME_NUM') == int(seoulpark_num)) \
                        .where(col('STD_DATE') <= dt.datetime(2022, 6, 30)) \
                        .sort(col('STD_DATE').desc())

        # 지하철 승하차수 데이터 가져오기
        df_subway = find_data(DataWarehouse, "SUBWAY_INOUT")
        df_subway = df_subway.select(col('STD_DATE'), col('IN_NUM').alias('SBW_IN_NUM'), col('OUT_NUM').alias('SBW_OUT_NUM')) \
                            .where(col('THEME_NUM') == int(seoulpark_num)) \
                            .where(col('STD_DATE') <= dt.datetime(2022, 6, 30)) \
                            .sort(col('STD_DATE').desc())

        # 이벤트 데이터 가져오기
        df_event = find_data(DataWarehouse, "THEME_EVENT")
        df_event = df_event.select(col('STD_DATE'), col('EVENT_OX')) \
                            .where(col('THEME_NUM') == int(seoulpark_num)) \
                            .where(col('STD_DATE') <= dt.datetime(2022, 6, 30)) \
                            .sort(col('STD_DATE').desc())

        # 이벤트 데이터 가져오기
        df_nav = find_data(DataWarehouse, "NAVI_SEARCH")
        df_nav = df_nav.select(col('STD_DATE'), col('SRC_NUM')) \
                            .where(col('THEME_NUM') == int(seoulpark_num)) \
                            .where(col('STD_DATE') <= dt.datetime(2022, 6, 30)) \
                            .sort(col('STD_DATE').desc())

        # 날짜만 가져오기
        dates = [row['STD_DATE'] for row in df_weather.collect()]

        # 요일 추가
        for i in range(len(dates)):
            dates[i] = (dates[i], dt.date.weekday(dates[i]) + 1)

        df_dates = get_spark_session().createDataFrame(dates, ['STD_DATE', 'DAY'])

        # 조인
        df_fin = df_ent.join(df_weather, on='STD_DATE')
        df_fin = df_fin.join(df_air, on='STD_DATE')
        df_fin = df_fin.join(df_subway, on='STD_DATE')
        df_fin = df_fin.join(df_event, on='STD_DATE')
        df_fin = df_fin.join(df_nav, on='STD_DATE')
        df_fin = df_fin.join(df_dates, on='STD_DATE')

        df_fin = df_fin.withColumn("STD_DATE", col('STD_DATE').cast('date'))
        df_fin.show()
        print(df_fin.dtypes)

        overwrite_trunc_data(DataMart, df_fin, 'TEST')