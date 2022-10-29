from infra.jdbc import DataMart, DataWarehouse, OperationDB, save_data
from pyspark.sql import Row
from infra.spark_session import get_spark_session
from pyspark.sql.functions import col
from pyspark.sql.types import *
import csv

class LottepriceTransformer:
    
    @classmethod
    def transform(cls):
        path = '/themapark/data/lotte_price.csv'
        price = get_spark_session().read.csv(path, encoding='cp949',header=True)

        p_data = price.select(
                col('PRICE').cast(IntegerType())
                ,col('AGES').cast(StringType())
                ,col('TICKET_GUBUN').cast(StringType()))
        p_data.printSchema()

        save_data(OperationDB,p_data , 'LOTTEWORLD_PRC')