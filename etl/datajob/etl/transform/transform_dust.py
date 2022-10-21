from infra.jdbc import DataWarehouse, save_data
from pyspark.sql import Row
from infra.spark_session import get_spark_session
from infra.util import cal_std_day
from pyspark.sql.functions import col
from pyspark.sql.types import *

class DustTransformer:

    @classmethod
    def transform(cls):
        path = '/themapark/dust/dust' + cal_std_day(0) + '.json'
        code_json = get_spark_session().read.json(path, encoding='UTF-8')
        data = []

        for r1 in code_json.select(code_json.data).toLocalIterator():
            if not r1.data:
                continue
            for r2 in r1.data:
                temp = r2.asDict()
                data.append(temp)
            
                dd = get_spark_session().createDataFrame(data)
                dd.show(3)

            w_data = dd.select(
                col('지역').cast(IntegerType()).alias('THEME_NUM')
                ,col('날짜').cast(DateType()).alias('STD_DATE')
                ,col('미세먼지').cast(IntegerType()).alias('PM10')
                ,col('초미세먼지').cast(IntegerType()).alias('PM25')
            )

            w_data.printSchema()

            save_data(DataWarehouse,w_data , 'DAILY_AIR')