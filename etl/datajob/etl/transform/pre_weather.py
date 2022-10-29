from infra.jdbc import DataMart, DataWarehouse, overwrite_data, overwrite_trunc_data, save_data
from pyspark.sql import Row
from infra.spark_session import get_spark_session
from infra.util import cal_std_day
from pyspark.sql.functions import col
from pyspark.sql.types import *

class PreweatherTransformer:

    @classmethod
    def transform(cls):
        path = '/themapark/weather/pre_weather' + cal_std_day(0) + '.json'
        code_json = get_spark_session().read.json(path, encoding='UTF-8')
        data = []

        for r1 in code_json.select(code_json.data).toLocalIterator():
            if not r1.data:
                continue
            for r2 in r1.data:
                temp = r2.asDict()
                data.append(temp)
            
                dw = get_spark_session().createDataFrame(data)
                dw.show(3)
  

            w_data = dw.select(
                dw.지역.cast(IntegerType()).alias('THEME_NUM')
                ,col('날짜').cast(DateType()).alias('STD_DATE')
                ,col('최고기온').cast(FloatType()).alias('HIGH_TEMP')
                ,col('최저기온').cast(FloatType()).alias('LOW_TEMP')
                ,col('일교차').cast(FloatType()).alias('DIFF_TEMP')
                ,col('강수량').cast(FloatType()).alias('RAIN_AMOUNT')
                ,col('바람').cast(FloatType()).alias('AVG_WIND')
                ,col('최대풍속').cast(FloatType()).alias('HIGH_WIND')
            )

            w_data.printSchema()

            overwrite_trunc_data(DataMart,w_data , 'DAILY_WEATHER')