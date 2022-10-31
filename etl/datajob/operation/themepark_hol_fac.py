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
            # 에버랜드 운휴시설
            file_name = cls.FILE_DIR + 'everland/' + 'holiday_area_everland_' + cal_std_day_after(i) + '.csv'
            df_everland = get_spark_session().read.csv(file_name, encoding='CP949', header=True)
            everland_info = df_everland.collect()
            for everland in everland_info:
                tmp_dict = {}
                tmp_dict = {'THEME_NAME': '에버랜드', 'FAC_NAME': everland[0], 'STD_DATE': cal_std_day_after2(i)}
                data.append(tmp_dict)

            # 롯데월드 운휴시설
            file_name = cls.FILE_DIR + 'lotteworld/' + 'holiday_area_lotteworld_' + cal_std_day_after(i) + '.csv'
            df_lotteworld = get_spark_session().read.csv(file_name, encoding='CP949', header=True)
            lotteworld_info = df_lotteworld.collect()
            for lotteworld in lotteworld_info:
                tmp_dict = {}
                tmp_dict = {'THEME_NAME': '롯데월드', 'FAC_NAME': lotteworld[0], 'STD_DATE': cal_std_day_after2(i)}
                data.append(tmp_dict)

        # DB에 저장
        df_fin = get_spark_session().createDataFrame(data)
        df_fin = df_fin.select(col('THEME_NAME'), to_date(col('STD_DATE'), 'yyyy-MM-dd').alias('STD_DATE'), col('FAC_NAME'))
        overwrite_trunc_data(OperationDB, df_fin, "THEMEPARK_HOLFAC")
