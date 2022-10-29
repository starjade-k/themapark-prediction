from etl.infra.jdbc import OperationDB
from infra.jdbc import DataMart, DataWarehouse, OperationDB, save_data
from pyspark.sql import Row
from infra.spark_session import get_spark_session
from pyspark.sql.functions import col
from pyspark.sql.types import *
import csv

class ChildparkingTransformer:
    
    @classmethod
    def transform(cls):
        path = '/themapark/data/child_parking.csv'
        parking = get_spark_session().read.csv(path, encoding='cp949',header=True)

        p_data = parking.select(
                col('PARKING_LOC').cast(StringType())
                ,col('PARKING_NUM').cast(IntegerType())
                ,col('PARKING_AREA').cast(IntegerType()))
        p_data.printSchema()

        save_data(OperationDB,p_data , 'CHILDPARK_PARKING')