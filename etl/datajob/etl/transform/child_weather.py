from infra.jdbc import DataMart, DataWarehouse, save_data
from pyspark.sql import Row
from infra.spark_session import get_spark_session
from pyspark.sql.functions import col
from pyspark.sql.types import *
import csv

class ChildweatherTransformer:
    
    @classmethod
    def transform(cls):
        path = '/themapark/data/child_weather.csv'
        dw = get_spark_session().read.csv(path, encoding='cp949',header=True)

        w_data = dw.select(
                dw.지점명.cast(IntegerType()).alias('THEME_NUM')
                ,col('date').cast(DateType()).alias('STD_DATE')
                ,col('최고기온(℃)').cast(FloatType()).alias('HIGH_TEMP')
                ,col('최저기온(℃)').cast(FloatType()).alias('LOW_TEMP')
                ,col('DIFF_TEMP').cast(FloatType())
                ,col('강수량(mm)').cast(FloatType()).alias('RAIN_AMOUNT')
                ,col('평균풍속(m/s)').cast(FloatType()).alias('AVG_WIND')
                ,col('최대풍속(m/s)').cast(FloatType()).alias('HIGH_WIND')
            )


        save_data(DataWarehouse,w_data , 'DAILY_WEATHER')