from pyspark.sql.functions import col, to_date
from infra.jdbc import OperationDB, overwrite_trunc_data
from infra.spark_session import get_spark_session
from infra.util import cal_std_day, cal_std_day2, cal_std_day_after, cal_std_day_after2


class ThemeparkHolFac:
    FILE_DIR = '/theme_park/info/'
    @classmethod
    def save(cls, after_cnt=7):
        data = []

        for i in range(0, after_cnt):
            cls.__everland_fac(data, i)
            cls.__lotteworld_fac(data, i)

        # 운영DB에 저장
        df_fin = get_spark_session().createDataFrame(data)
        df_fin = df_fin.select(col('THEME_NAME'), to_date(col('STD_DATE'), 'yyyy-MM-dd').alias('STD_DATE'), col('FAC_NAME'))
        overwrite_trunc_data(OperationDB, df_fin, "THEMEPARK_HOLFAC")

    # 롯데월드 운휴시설 데이터 가공
    @classmethod
    def __lotteworld_fac(cls, data, i):
        df_lotteworld = cls.__get_lotteworld_data_from_hdfs(i)
        lotteworld_info = df_lotteworld.collect()
        for lotteworld in lotteworld_info:
            tmp_dict = {}
            tmp_dict = {'THEME_NAME': '롯데월드', 'FAC_NAME': lotteworld[0], 'STD_DATE': cal_std_day_after2(i)}
            data.append(tmp_dict)

    # HDFS에서 롯데월드 데이터 가져와 데이터프레임으로 생성
    @classmethod
    def __get_lotteworld_data_from_hdfs(cls, i):
        file_name = cls.FILE_DIR + 'lotteworld/' + 'holiday_area_lotteworld_' + cal_std_day_after(i) + '.csv'
        df_lotteworld = get_spark_session().read.csv(file_name, encoding='CP949', header=True)
        return df_lotteworld

    # 에버랜드 운휴시설 데이터 가공
    @classmethod
    def __everland_fac(cls, data, i):
        df_everland = cls.__get_everland_data_from_hdfs(i)
        everland_info = df_everland.collect()
        for everland in everland_info:
            tmp_dict = {}
            tmp_dict = {'THEME_NAME': '에버랜드', 'FAC_NAME': everland[0], 'STD_DATE': cal_std_day_after2(i)}
            data.append(tmp_dict)

    # HDFS에서 에버랜드 데이터 가져와 데이터프레임으로 생성
    @classmethod
    def __get_everland_data_from_hdfs(cls, i):
        file_name = cls.FILE_DIR + 'everland/' + 'holiday_area_everland_' + cal_std_day_after(i) + '.csv'
        df_everland = get_spark_session().read.csv(file_name, encoding='CP949', header=True)
        return df_everland
