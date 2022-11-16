import datetime as dt
from pyspark.sql.functions import col, to_date
from infra.jdbc import find_data, DataWarehouse, DataMart, overwrite_trunc_data
from infra.spark_session import get_spark_session

class PreChildParkTransformer:
    @classmethod
    def transform(cls):
        childpark_num = cls.__get_theme_num()

        # 입장객수 데이터 가져오기
        df_ent = cls.__get_entrance(childpark_num)

        # 날씨 데이터 가져오기
        df_weather = cls.__get_weather(childpark_num)

        # 미세먼지 데이터 가져오기
        df_air = cls.__get_air(childpark_num)

        # 지하철 승하차수 데이터 가져오기
        df_subway = cls.__get_subway(childpark_num)

        # 이벤트 데이터 가져오기
        df_event = cls.__get_event(childpark_num)

        # 네비게이션 데이터 가져오기
        df_nav = cls.__get_navigation(childpark_num)

        # 공휴일 데이터 가져오기
        df_holiday = cls.__get_holiday()

        # 코로나 확진자 수 데이터 가져오기
        df_corona = cls.__get_corona()

        # 날짜만 가져오기
        dates = [row['STD_DATE'] for row in df_weather.collect()]

        # 요일 추가
        df_dates = cls.__create_yoil(dates)

        # 조인
        df_fin = cls.__join_datas(df_ent, df_weather, df_air, df_subway, df_event, df_nav, df_holiday, df_corona, df_dates)

        # DM에 저장
        overwrite_trunc_data(DataMart, df_fin, 'PRE_CHILDPARK')

    @classmethod
    def __join_datas(cls, df_ent, df_weather, df_air, df_subway, df_event, df_nav, df_holiday, df_corona, df_dates):
        df_fin = df_ent.join(df_weather, on='STD_DATE')
        df_fin = df_fin.join(df_air, on='STD_DATE')
        df_fin = df_fin.join(df_subway, on='STD_DATE')
        df_fin = df_fin.join(df_event, on='STD_DATE')
        df_fin = df_fin.join(df_nav, on='STD_DATE')
        df_fin = df_fin.join(df_holiday, on='STD_DATE')
        df_fin = df_fin.join(df_corona, on='STD_DATE')
        df_fin = df_fin.join(df_dates, on='STD_DATE')

        df_fin = df_fin.withColumn("STD_DATE", col('STD_DATE').cast('date'))
        df_fin.show()
        print(df_fin.dtypes)
        return df_fin

    @classmethod
    def __create_yoil(cls, dates):
        for i in range(len(dates)):
            dates[i] = (dates[i], dt.date.weekday(dates[i]) + 1)

        df_dates = get_spark_session().createDataFrame(dates, ['STD_DATE', 'DAY'])
        return df_dates

    @classmethod
    def __get_corona(cls):
        df_corona = find_data(DataWarehouse, "SEOUL_CORONA")
        df_corona = df_corona.select(col('STD_DATE'), col('PATIENT').alias('CORONA_PAT')) \
                            .where(col('STD_DATE') <= dt.datetime(2022, 6, 30)) \
                            .sort(col('STD_DATE').desc())
                            
        return df_corona

    @classmethod
    def __get_holiday(cls):
        df_holiday = find_data(DataWarehouse, "HOLIDAY")
        df_holiday = df_holiday.select(col('STD_DATE'), col('HOLIDAY_OX')) \
                            .where(col('STD_DATE') <= dt.datetime(2022, 6, 30)) \
                            .sort(col('STD_DATE').desc())
                            
        return df_holiday

    @classmethod
    def __get_navigation(cls, childpark_num):
        df_nav = find_data(DataWarehouse, "NAVI_SEARCH")
        df_nav = df_nav.select(col('STD_DATE'), col('SRC_NUM').alias('NAVI_SRC_NUM')) \
                            .where(col('THEME_NUM') == int(childpark_num)) \
                            .where(col('STD_DATE') <= dt.datetime(2022, 6, 30)) \
                            .sort(col('STD_DATE').desc())
                            
        return df_nav

    @classmethod
    def __get_event(cls, childpark_num):
        df_event = find_data(DataWarehouse, "THEME_EVENT")
        df_event = df_event.select(col('STD_DATE'), col('EVENT_OX')) \
                            .where(col('THEME_NUM') == int(childpark_num)) \
                            .where(col('STD_DATE') <= dt.datetime(2022, 6, 30)) \
                            .sort(col('STD_DATE').desc())
                            
        return df_event

    @classmethod
    def __get_subway(cls, childpark_num):
        df_subway = find_data(DataWarehouse, "SUBWAY_INOUT")
        df_subway = df_subway.select(col('STD_DATE'), col('IN_NUM').alias('SBW_IN_NUM'), col('OUT_NUM').alias('SBW_OUT_NUM')) \
                            .where(col('THEME_NUM') == int(childpark_num)) \
                            .where(col('STD_DATE') <= dt.datetime(2022, 6, 30)) \
                            .sort(col('STD_DATE').desc())
                            
        return df_subway

    @classmethod
    def __get_air(cls, childpark_num):
        df_air = find_data(DataWarehouse, "DAILY_AIR")
        df_air = df_air.select(col('STD_DATE'), col('PM10'), col('PM25')) \
                        .where(col('THEME_NUM') == int(childpark_num)) \
                        .where(col('STD_DATE') <= dt.datetime(2022, 6, 30)) \
                        .sort(col('STD_DATE').desc())
                        
        return df_air

    @classmethod
    def __get_weather(cls, childpark_num):
        df_weather = find_data(DataWarehouse, "DAILY_WEATHER")
        df_weather = df_weather.select(col('STD_DATE'), col('HIGH_TEMP'), col('LOW_TEMP'), col('RAIN_AMOUNT'), col('AVG_WIND'), col('HIGH_WIND')) \
                                .where(col('THEME_NUM') == int(childpark_num)) \
                                .where(col('STD_DATE') <= dt.datetime(2022, 6, 30)) \
                                .sort(col('STD_DATE').desc())
                                
        return df_weather

    @classmethod
    def __get_entrance(cls, childpark_num):
        df_ent = find_data(DataWarehouse, "THEME_ENTRANCE1")
        df_ent = df_ent.select(col('STD_DATE'), col('ENT_NUM')) \
                                .where(col('THEME_NUM') == int(childpark_num)) \
                                .where(col('STD_DATE') <= dt.datetime(2022, 6, 30)) \
                                .sort(col('STD_DATE').desc())
                                
        return df_ent

    @classmethod
    def __get_theme_num(cls):
        df_themepark = find_data(DataWarehouse, "THEMEPARK")

        # DB에서 테마파크 번호 가져오기
        childpark_num = df_themepark.where(col('THEME_NAME') == '서울어린이대공원').first()[0]
        return childpark_num