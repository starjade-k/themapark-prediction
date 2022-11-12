from infra.jdbc import DataMart, overwrite_trunc_data
from infra.spark_session import get_spark_session
from infra.util import cal_std_day
from pyspark.sql.functions import col
from pyspark.sql.types import *

class PreairweatherTransformer:

    @classmethod
    def transform(cls):
        path = '/themapark/dust/pre_dust' + cal_std_day(0) + '.json'
        code_json = get_spark_session().read.json(path, encoding='UTF-8')
        data = []

        for r1 in code_json.select(code_json.data).toLocalIterator():
            if not r1.data:
                continue
            for r2 in r1.data:
                temp = r2.asDict()
                data.append(temp)
            
                dd = get_spark_session().createDataFrame(data)
                dd.show(3)

            dust_data = dd.select(
                col('지역').cast(IntegerType()).alias('THEME_NUM')
                ,col('날짜').cast(DateType()).alias('STD_DATE')
                ,col('미세먼지').cast(IntegerType()).alias('PM10')
                ,col('초미세먼지').cast(IntegerType()).alias('PM25')
            )

        path2 = '/themapark/weather/pre_weather' + cal_std_day(0) + '.json'
        code_json = get_spark_session().read.json(path2, encoding='UTF-8')
        data = []

        for r1 in code_json.select(code_json.data).toLocalIterator():
            if not r1.data:
                continue
            for r2 in r1.data:
                temp = r2.asDict()
                data.append(temp)
                    
                dw = get_spark_session().createDataFrame(data)
                dw.show(3)
        

                weather_data = dw.select(
                    dw.지역.cast(IntegerType()).alias('THEME_NUM')
                    ,col('날짜').cast(DateType()).alias('STD_DATE')
                    ,col('최고기온').cast(FloatType()).alias('HIGH_TEMP')
                    ,col('최저기온').cast(FloatType()).alias('LOW_TEMP')
                    ,col('일교차').cast(FloatType()).alias('DIFF_TEMP')
                    ,col('강수량').cast(FloatType()).alias('RAIN_AMOUNT')
                    ,col('바람').cast(FloatType()).alias('AVG_WIND')
                    ,col('최대풍속').cast(FloatType()).alias('HIGH_WIND')
                )

                weather = weather_data
                dust = dust_data
                wd_data = weather.join(dust, (weather.STD_DATE == dust.STD_DATE) & (weather.THEME_NUM == dust.THEME_NUM) )\
                                .select(weather.STD_DATE,weather.THEME_NUM,'HIGH_TEMP','LOW_TEMP','DIFF_TEMP','RAIN_AMOUNT','AVG_WIND','HIGH_WIND',dust.PM10,dust.PM25)

                # DM에 저장
                overwrite_trunc_data(DataMart, wd_data, 'PRE_AIR_WEATHER')

            