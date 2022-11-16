from pyspark.sql.functions import col, lit, to_date
from pyspark.sql.types import IntegerType
from infra.jdbc import find_data, DataWarehouse, save_data
from infra.spark_session import get_spark_session

class PastAirDataTransformer:
    FILE_DIR = '/theme_park/past_weather/'

    @classmethod
    def transform(cls):
        seoulpark_num, childpark_num, lotteworld_num, everland_num = cls.__get_theme_num()

        seoulpark_filename = 'gwacheon_air_2017_202206.csv'
        childpark_filename = 'gwangjin_air_2017_202206.csv'
        lotteworld_filename = 'songpa_air_2017_202206.csv'
        everland_filename = 'yongin_air_2017_202206.csv'

        df_seoulpark = get_spark_session().read.csv(cls.FILE_DIR + seoulpark_filename, encoding='CP949', header=True)
        df_seoulpark = df_seoulpark.select(lit(seoulpark_num).cast(IntegerType()).alias('THEME_NUM'), to_date(col('STD_DATE'), 'yyyy-MM-dd').alias('STD_DATE'), 
                                            col('PM10').cast(IntegerType()).alias('PM10'), col('PM25').cast(IntegerType()).alias('PM25'))
        df_seoulpark.show()
        print(df_seoulpark.dtypes)
        save_data(DataWarehouse, df_seoulpark, "DAILY_AIR")

        df_childpark = get_spark_session().read.csv(cls.FILE_DIR + childpark_filename, encoding='CP949', header=True)
        df_childpark = df_childpark.select(lit(childpark_num).cast(IntegerType()).alias('THEME_NUM'), to_date(col('STD_DATE'), 'yyyy-MM-dd').alias('STD_DATE'), 
                                            col('PM10').cast(IntegerType()).alias('PM10'), col('PM25').cast(IntegerType()).alias('PM25'))
        df_childpark.show()
        print(df_childpark.dtypes)
        save_data(DataWarehouse, df_childpark, "DAILY_AIR")

        df_lotteworld = get_spark_session().read.csv(cls.FILE_DIR + lotteworld_filename, encoding='CP949', header=True)
        df_lotteworld = df_lotteworld.select(lit(lotteworld_num).cast(IntegerType()).alias('THEME_NUM'), to_date(col('STD_DATE'), 'yyyy-MM-dd').alias('STD_DATE'), 
                                            col('PM10').cast(IntegerType()).alias('PM10'), col('PM25').cast(IntegerType()).alias('PM25'))
        df_lotteworld.show()
        print(df_lotteworld.dtypes)
        save_data(DataWarehouse, df_lotteworld, "DAILY_AIR")

        df_everland = get_spark_session().read.csv(cls.FILE_DIR + everland_filename, encoding='CP949', header=True)
        df_everland = df_everland.select(lit(everland_num).cast(IntegerType()).alias('THEME_NUM'), to_date(col('STD_DATE'), 'yyyy-MM-dd').alias('STD_DATE'), 
                                            col('PM10').cast(IntegerType()).alias('PM10'), col('PM25').cast(IntegerType()).alias('PM25'))
        df_everland.show()
        print(df_everland.dtypes)
        save_data(DataWarehouse, df_everland, "DAILY_AIR")

    @classmethod
    def __get_theme_num(cls):
        df_themepark = find_data(DataWarehouse, "THEMEPARK")
        df_themepark.show()

        # db에서 테마파크 번호 가져오기
        seoulpark_num = df_themepark.where(col('THEME_NAME') == '서울대공원').first()[0]
        childpark_num = df_themepark.where(col('THEME_NAME') == '서울어린이대공원').first()[0]
        lotteworld_num = df_themepark.where(col('THEME_NAME') == '롯데월드').first()[0]
        everland_num = df_themepark.where(col('THEME_NAME') == '에버랜드').first()[0]
        return seoulpark_num,childpark_num,lotteworld_num,everland_num
