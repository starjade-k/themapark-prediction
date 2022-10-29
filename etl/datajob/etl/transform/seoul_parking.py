from infra.jdbc import DataMart, DataWarehouse, OpData, save_data
from pyspark.sql import Row
from infra.spark_session import get_spark_session
from pyspark.sql.functions import col
from pyspark.sql.types import *
import csv

class SeoulparkingTransformer:
    
    @classmethod
    def transform(cls):
        path = '/themapark/data/seoul_parking.csv'
        parking = get_spark_session().read.csv(path, encoding='cp949',header=True)

        p_data = parking.select(
                col('PARKING_LOC').cast(StringType()).alias('PARKING_GUBUN')
                ,col('PARKING_NUM').cast(IntegerType())
                ,col('PARKING_AREA').cast(IntegerType()))
        p_data.printSchema()

        save_data(OpData,p_data , 'SEOULPARK_PARKING')