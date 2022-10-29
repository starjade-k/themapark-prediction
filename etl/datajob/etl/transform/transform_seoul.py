from infra.jdbc import DataWarehouse, save_data
from pyspark.sql import Row
from infra.spark_session import get_spark_session
from pyspark.sql.functions import col
from pyspark.sql.types import *
import csv

class SeoulTransformer:

    @classmethod
    def transform(cls):
        path = '/themapark/data/seoul2.csv/'
        seoul = get_spark_session().read.csv(path, encoding='cp949',header=True)

        s_data = seoul.select(
                col('Daily_Total').cast(IntegerType()).alias('ENT_NUM')
                ,col('date').cast(DateType()).alias('STD_DATE')
                ,col('THEME_NUM').cast(IntegerType())
            )

        s_data.printSchema()

        save_data(DataWarehouse,s_data , 'THEME_ENTRANCE')