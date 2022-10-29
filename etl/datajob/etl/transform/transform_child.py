from infra.jdbc import DataWarehouse, save_data
from pyspark.sql import Row
from infra.spark_session import get_spark_session
from pyspark.sql.functions import col
from pyspark.sql.types import *
import csv

class ChildTransformer:

    @classmethod
    def transform(cls):
        path = '/themapark/data/childpark2.csv/'
        child = get_spark_session().read.csv(path, encoding='cp949',header=True)

        c_data = child.select(
                col('총 입장객').cast(IntegerType()).alias('ENT_NUM')
                ,col('날짜').cast(DateType()).alias('STD_DATE')
                ,col('THEME_NUM').cast(IntegerType())
            )

        c_data.printSchema()

        save_data(DataWarehouse,c_data , 'THEME_ENTRANCE')