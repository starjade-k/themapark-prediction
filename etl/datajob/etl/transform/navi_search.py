from pyspark.sql.functions import col, lit, to_date, concat
from pyspark.sql.types import IntegerType
from infra.jdbc import DataWarehouse, find_data, save_data
from infra.spark_session import get_spark_session
from infra.util import cal_std_day


class NaviSearchTransformer:
    FILE_DIR = '/theme_park/navigation/'
    @classmethod
    def transform(cls, before_cnt=2):
        df_themepark = find_data(DataWarehouse, "THEMEPARK")
        df_themepark.show()

        # db에서 테마파크 번호 가져오기
        everland_num = df_themepark.where(col('THEME_NAME') == '에버랜드').first()[0]
        seoulpark_num = df_themepark.where(col('THEME_NAME') == '서울대공원').first()[0]
        childpark_num = df_themepark.where(col('THEME_NAME') == '서울어린이대공원').first()[0]
        lotteworld_num = df_themepark.where(col('THEME_NAME') == '롯데월드').first()[0]

        # hdfs 읽어오기
        file_name = cls.FILE_DIR + 'navi_search_' + cal_std_day(before_cnt) + '.csv'
        df_navi = get_spark_session().read.csv(file_name, encoding='CP949', header=True)
        df_navi.show(5)

        # # 각 테마파크별로 db에 넣기
        # df_everland = df_navi.select(lit(everland_num).cast(IntegerType()).alias('THEME_NUM'),
        #                             to_date(concat(col('날짜').substr(1, 4), lit('-'), col('날짜').substr(5, 2), lit('-'), col('날짜').substr(7, 2)), 'yyyy-MM-dd').alias('STD_DATE'),
        #                             col('에버랜드').cast(IntegerType()).alias('SRC_NUM'))
        # df_everland.show(5)
        # print(df_everland.dtypes)
        # save_data(DataWarehouse, df_everland, 'NAVI_SEARCH')

        # df_seoulpark = df_navi.select(lit(seoulpark_num).cast(IntegerType()).alias('THEME_NUM'),
        #                             to_date(concat(col('날짜').substr(1, 4), lit('-'), col('날짜').substr(5, 2), lit('-'), col('날짜').substr(7, 2)), 'yyyy-MM-dd').alias('STD_DATE'),
        #                             col('서울대공원').cast(IntegerType()).alias('SRC_NUM'))
        # save_data(DataWarehouse, df_seoulpark, 'NAVI_SEARCH')

        # df_childpark = df_navi.select(lit(childpark_num).cast(IntegerType()).alias('THEME_NUM'),
        #                             to_date(concat(col('날짜').substr(1, 4), lit('-'), col('날짜').substr(5, 2), lit('-'), col('날짜').substr(7, 2)), 'yyyy-MM-dd').alias('STD_DATE'),
        #                             col('서울어린이대공원').cast(IntegerType()).alias('SRC_NUM'))
        # save_data(DataWarehouse, df_childpark, 'NAVI_SEARCH')

        # df_lotteword = df_navi.select(lit(lotteworld_num).cast(IntegerType()).alias('THEME_NUM'),
        #                             to_date(concat(col('날짜').substr(1, 4), lit('-'), col('날짜').substr(5, 2), lit('-'), col('날짜').substr(7, 2)), 'yyyy-MM-dd').alias('STD_DATE'),
        #                             col('롯데월드').cast(IntegerType()).alias('SRC_NUM'))
        # save_data(DataWarehouse, df_lotteword, 'NAVI_SEARCH')

        # 각 테마파크별로 db에 넣기
        df_everland = df_navi.select(lit(everland_num).cast(IntegerType()).alias('THEME_NUM'),
                                    to_date(col('날짜'), 'yyyy-MM-dd').alias('STD_DATE'),
                                    col('에버랜드').cast(IntegerType()).alias('SRC_NUM'))
        df_everland.show(5)
        print(df_everland.dtypes)
        save_data(DataWarehouse, df_everland, 'NAVI_SEARCH')

        df_seoulpark = df_navi.select(lit(seoulpark_num).cast(IntegerType()).alias('THEME_NUM'),
                                    to_date(col('날짜'), 'yyyy-MM-dd').alias('STD_DATE'),
                                    col('서울대공원').cast(IntegerType()).alias('SRC_NUM'))
        save_data(DataWarehouse, df_seoulpark, 'NAVI_SEARCH')

        df_childpark = df_navi.select(lit(childpark_num).cast(IntegerType()).alias('THEME_NUM'),
                                    to_date(col('날짜'), 'yyyy-MM-dd').alias('STD_DATE'),
                                    col('서울어린이대공원').cast(IntegerType()).alias('SRC_NUM'))
        save_data(DataWarehouse, df_childpark, 'NAVI_SEARCH')

        df_lotteword = df_navi.select(lit(lotteworld_num).cast(IntegerType()).alias('THEME_NUM'),
                                    to_date(col('날짜'), 'yyyy-MM-dd').alias('STD_DATE'),
                                    col('롯데월드').cast(IntegerType()).alias('SRC_NUM'))
        save_data(DataWarehouse, df_lotteword, 'NAVI_SEARCH')

        
