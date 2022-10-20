import datetime as dt
from pyspark.sql.functions import col, lit
from infra.jdbc import DataWarehouse, find_data
from infra.spark_session import get_spark_session
from infra.util import cal_std_day


class ThemeParkEventTransformer:
    FILE_DIR = '/theme_park/event/'

    @classmethod
    def transform(cls):
        df_themepark = find_data(DataWarehouse, "THEMEPARK")
        df_themepark.show()

        # db에서 테마파크 번호 가져오기
        everland_num = df_themepark.where(col('THEME_NAME') == '에버랜드').first()[0]
        seoulpark_num = df_themepark.where(col('THEME_NAME') == '서울대공원').first()[0]
        childpark_num = df_themepark.where(col('THEME_NAME') == '서울어린이대공원').first()[0]
        lotteworld_num = df_themepark.where(col('THEME_NAME') == '롯데월드').first()[0]

        everland_file_name = cls.FILE_DIR + 'everland/' + 'everland_event_2018_2022.csv'
        df_everland = get_spark_session().read.csv(everland_file_name, encoding='CP949', header=True)
        df_everland.show(5)
        
        #cls.__create_df_with_eventdata()

    @classmethod
    def __create_df_with_eventdata(cls, theme_num, events_data):
        tmp_dict = {'THEME_NUM': [], 'STD_DATE': [], 'EVENT_OX': [], 'EVENTNAME': []}
        for i in range(2115, 108, -1):  # 1748, 106, -1 
            day = cal_std_day(i)
            tmp_dict['날짜'].append(day)
            for k in range(len(events_data)):
                startdate = str(events_data[k][1])
                enddate = str(events_data[k][2])
                date1 = dt.datetime(int(startdate[:4]), int(startdate[4:6]), int(startdate[6:8]))
                date2 = dt.datetime(int(enddate[:4]), int(enddate[4:6]), int(enddate[6:8]))
                d = dt.datetime(int(day[:4]), int(day[4:6]), int(day[6:8]))
                if date1 <= d <= date2:
                    tmp_dict['행사ox'].append('o')
                    tmp_dict['행사명'].append(events_data[k][0])
                    break
            else:
                tmp_dict['행사ox'].append('x')
                tmp_dict['행사명'].append('')
        df_seoulpark_fin = pd.DataFrame(tmp_dict)