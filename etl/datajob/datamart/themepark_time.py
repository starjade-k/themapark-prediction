from pyspark.sql.functions import col, to_date
from infra.jdbc import DataMart, overwrite_trunc_data
from infra.spark_session import get_spark_session
from infra.util import cal_std_day

class ThemeparkTime:
    FILE_DIR = '/theme_park/info/'

    @classmethod
    def save(cls):
        today = cal_std_day(0)
        today = today[:4] + '-' + today[4:6] + '-' + today[6:8]

        data = []
        # 에버랜드 이용시간
        file_name = cls.FILE_DIR + 'everland/' + 'time_everland_20221026.csv'
        df_everland = get_spark_session().read.csv(file_name, encoding='CP949', header=True)
        everland_info = df_everland.collect()
        tmp_dict = {'THEME_NAME': '에버랜드', 'STD_DATE': today, 'START_TIME': everland_info[0][0], 'END_TIME': everland_info[0][1]}
        data.append(tmp_dict)

        # 롯데월드 이용시간
        file_name = cls.FILE_DIR + 'everland/' + 'time_everland_20221026.csv'
        df_lotteworld = get_spark_session().read.csv(file_name, encoding='CP949', header=True)
        lotteworld_info = df_lotteworld.collect()
        tmp_dict = {'THEME_NAME': '롯데월드', 'STD_DATE': today, 'START_TIME': lotteworld_info[0][0], 'END_TIME': lotteworld_info[0][1]}
        data.append(tmp_dict)

        # 서울대공원 이용시간
        tmp_dict = {'THEME_NAME': '서울대공원', 'STD_DATE': today, 'START_TIME': '09:00'}
        today_month = int(cal_std_day(0)[4:6])
        if today_month >= 5 and today_month <= 8:
            tmp_dict['END_TIME'] = '19:00'
        elif today_month >= 11 and today_month <= 2:
            tmp_dict['END_TIME'] = '17:00'
        else:
            tmp_dict['END_TIME'] = '18:00'
        data.append(tmp_dict)
        tmp_dict = {'THEME_NAME': '서울대공원 전시온실', 'STD_DATE': today, 'START_TIME': '10:00', 'END_TIME': '16:00'}
        data.append(tmp_dict)

        # 서울어린이대공원 이용시간
        tmp_dict = {'THEME_NAME': '서울어린이대공원', 'STD_DATE': today, 'START_TIME': '05:00', 'END_TIME': '22:00'}
        data.append(tmp_dict)
        tmp_dict = {'THEME_NAME': '서울어린이대공원 동물원', 'STD_DATE': today, 'START_TIME': '10:00', 'END_TIME': '17:00'}
        data.append(tmp_dict)

        # DM에 저장
        df_fin = get_spark_session().createDataFrame(data)
        df_fin = df_fin.select(col('THEME_NAME'), to_date(col('STD_DATE'), 'yyyy-MM-dd').alias('STD_DATE'),
                                col('START_TIME'), col('END_TIME'))
        overwrite_trunc_data(DataMart, df_fin, "THEMEPARK_TIME")
