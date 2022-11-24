from pyspark.sql.functions import col, lit, to_date
from pyspark.sql.types import IntegerType
from infra.jdbc import DataWarehouse, find_data, save_data
from infra.spark_session import get_spark_session
from infra.util import cal_std_day2


class NaviSearchTransformer:
    FILE_DIR = '/theme_park/navigation/'
    @classmethod
    def transform(cls, before_cnt=2):
        
        everland_num, seoulpark_num, childpark_num, lotteworld_num = cls.__get_thme_num()

        df_navi = cls.__get_data_from_hdfs(before_cnt)

        # 각 테마파크별로 db에 넣기
        cls.__save_everland_data(everland_num, df_navi)

        cls.__save_seoulpark_data(seoulpark_num, df_navi)

        cls.__save_childpark_data(childpark_num, df_navi)

        cls.__save_lotteworld_data(lotteworld_num, df_navi)

    # 롯데월드 데이터 DW에 저장
    @classmethod
    def __save_lotteworld_data(cls, lotteworld_num, df_navi):
        df_lotteword = df_navi.select(lit(lotteworld_num).cast(IntegerType()).alias('THEME_NUM'),
                                    to_date(col('날짜'), 'yyyy-MM-dd').alias('STD_DATE'),
                                    col('롯데월드').cast(IntegerType()).alias('SRC_NUM'))
        save_data(DataWarehouse, df_lotteword, 'NAVI_SEARCH')

    # 어린이대공원 데이터 DW에 저장
    @classmethod
    def __save_childpark_data(cls, childpark_num, df_navi):
        df_childpark = df_navi.select(lit(childpark_num).cast(IntegerType()).alias('THEME_NUM'),
                                    to_date(col('날짜'), 'yyyy-MM-dd').alias('STD_DATE'),
                                    col('서울어린이대공원').cast(IntegerType()).alias('SRC_NUM'))
        save_data(DataWarehouse, df_childpark, 'NAVI_SEARCH')

    # 서울대공원 데이터 DW에 저장
    @classmethod
    def __save_seoulpark_data(cls, seoulpark_num, df_navi):
        df_seoulpark = df_navi.select(lit(seoulpark_num).cast(IntegerType()).alias('THEME_NUM'),
                                    to_date(col('날짜'), 'yyyy-MM-dd').alias('STD_DATE'),
                                    col('서울대공원').cast(IntegerType()).alias('SRC_NUM'))
        save_data(DataWarehouse, df_seoulpark, 'NAVI_SEARCH')

    # 에버랜드 데이터 DW에 저장
    @classmethod
    def __save_everland_data(cls, everland_num, df_navi):
        df_everland = df_navi.select(lit(everland_num).cast(IntegerType()).alias('THEME_NUM'),
                                    to_date(col('날짜'), 'yyyy-MM-dd').alias('STD_DATE'),
                                    col('에버랜드').cast(IntegerType()).alias('SRC_NUM'))
        save_data(DataWarehouse, df_everland, 'NAVI_SEARCH')

    # HDFS에서 데이터 가져와 데이터프레임으로 생성
    @classmethod
    def __get_data_from_hdfs(cls, before_cnt):
        file_name = cls.FILE_DIR + 'navi_search_' + cal_std_day2(before_cnt) + '.csv'
        df_navi = get_spark_session().read.csv(file_name, encoding='CP949', header=True)
        df_navi.show(5)
        return df_navi

    # DW에서 테마파크 번호 가져오기
    @classmethod
    def __get_thme_num(cls):
        df_themepark = find_data(DataWarehouse, "THEMEPARK")
        df_themepark.show()

        everland_num = df_themepark.where(col('THEME_NAME') == '에버랜드').first()[0]
        seoulpark_num = df_themepark.where(col('THEME_NAME') == '서울대공원').first()[0]
        childpark_num = df_themepark.where(col('THEME_NAME') == '서울어린이대공원').first()[0]
        lotteworld_num = df_themepark.where(col('THEME_NAME') == '롯데월드').first()[0]
        return everland_num,seoulpark_num,childpark_num,lotteworld_num

        
