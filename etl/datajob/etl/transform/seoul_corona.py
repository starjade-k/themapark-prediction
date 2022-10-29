from infra.jdbc import DataMart, DataWarehouse, save_data
from pyspark.sql import Row
from infra.spark_session import get_spark_session
from pyspark.sql.functions import col
from pyspark.sql.types import *
import csv

class SeoulcoronaTransformer:
    
    @classmethod
    def transform(cls):
        path = '/themapark/data/seoul_corona.csv'
        parking = get_spark_session().read.csv(path, encoding='cp949',header=True)

        p_data = parking.select(
                col('자치구 기준일').cast(DateType()).alias('STD_DATE')
                ,col('일일 증가량').cast(IntegerType()).alias('PATIENT'))
        p_data.printSchema()

        save_data(DataWarehouse,p_data , 'SEOUL_CORONA')