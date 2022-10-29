from infra.jdbc import DataWarehouse, save_data
from pyspark.sql import Row
from infra.spark_session import get_spark_session
from pyspark.sql.functions import col
from pyspark.sql.types import *
import csv
class SubwayTransformer:

    @classmethod
    def transform(cls):
        path = '/themapark/data/final_subway.csv'
        subway = get_spark_session().read.csv(path, encoding='cp949',header=True)

        s_data = subway.select(
            col('역명').cast(IntegerType()).alias('THEME_NUM')
            ,col('사용일자').cast(DateType()).alias('STD_DATE')
            ,col('승차총승객수').cast(IntegerType()).alias('IN_NUM')
            ,col('하차총승객수').cast(IntegerType()).alias('OUT_NUM')
        )
        s_data.printSchema()

        save_data(DataWarehouse,s_data , 'SUBWAY_INOUT')