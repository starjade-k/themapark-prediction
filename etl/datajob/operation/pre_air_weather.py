from infra.jdbc import OperationDB, DataWarehouse, overwrite_trunc_data, find_data
from pyspark.sql import Row
from infra.spark_session import get_spark_session
from infra.util import cal_std_day
from pyspark.sql.functions import col
from pyspark.sql.types import *

class PreairweatherOperation:

    @classmethod
    def save(cls):
        path = '/themapark/dust/pre_dust' + cal_std_day(0) + '.json'
        code_json = get_spark_session().read.json(path, encoding='UTF-8')
        data = []

        # 테마파크 이름 가져오기
        themepark = find_data(DataWarehouse, "THEMEPARK").select('THEME_NUM', 'THEME_NAME')
        themepark.show()


        for r1 in code_json.select(code_json.data).toLocalIterator():
            if not r1.data:
                continue
            for r2 in r1.data:
                temp = r2.asDict()
                data.append(temp)
            
                dd = get_spark_session().createDataFrame(data)
                #dd.show(3)

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
        
                weather_data = dw.select(
                    dw.지역.cast(IntegerType()).alias('THEME_NUM')
                    ,col('날짜').cast(DateType()).alias('STD_DATE')
                    ,col('최고기온').cast(FloatType()).alias('HIGH_TEMP')
                    ,col('최저기온').cast(FloatType()).alias('LOW_TEMP')
                    ,col('일교차').cast(FloatType()).alias('DIFF_TEMP')
                    ,col('강수량').cast(FloatType()).alias('RAIN_AMOUNT')
                    ,col('바람').cast(FloatType()).alias('AVG_WIND')
                    ,col('최대풍속').cast(FloatType()).alias('HIGH_WIND')
                    ,col('img').cast(StringType()).alias('WEATHER_IMG')
                )

                weather = weather_data
                dust = dust_data
                wd_data = weather.join(dust, (weather.STD_DATE == dust.STD_DATE) & (weather.THEME_NUM == dust.THEME_NUM) )\
                                .select(weather.STD_DATE,weather.THEME_NUM,weather.WEATHER_IMG,'HIGH_TEMP','LOW_TEMP','DIFF_TEMP','RAIN_AMOUNT','AVG_WIND','HIGH_WIND',dust.PM10,dust.PM25)


        res_data = wd_data.join(themepark, on='THEME_NUM').drop('THEME_NUM')
        res_data.show()
        # DM에 저장
        overwrite_trunc_data(OperationDB, res_data, 'PRE_AIR_WEATHER')


            