import datetime as dt
from pyspark.sql.functions import col, lit, to_date
from infra.jdbc import DataWarehouse, find_data, save_data
from infra.spark_session import get_spark_session
from infra.util import cal_std_day2


class PastThemeParkEventTransformer:
    FILE_DIR = '/theme_park/event/'

    @classmethod
    def transform(cls):
        cls.__get_theme_num()

        df_everland, df_seoulpark, df_lotteworld, df_childpark = cls.__get_data_from_hdfs()

        cls.__save_everland_data(df_everland)

        cls.__save_lotteworld_data(df_lotteworld)

        cls.__save_childpark_data(df_childpark)

        cls.__save_seoulpark_data(df_seoulpark)

    # 서울대공원 데이터 DW에 저장
    @classmethod
    def __save_seoulpark_data(cls, df_seoulpark):
        seoulpark_list = df_seoulpark.collect()
        df_seoulpark_fin = cls.__create_df_with_eventdata(seoulpark_num, seoulpark_list)
        df_seoulpark_fin = df_seoulpark_fin.select(col('THEME_NUM'), to_date(col('STD_DATE'), 'yyyy-MM-dd').alias('STD_DATE'),
                                                col('EVENT_OX'), col('EVENT_NAME'))                                          
        save_data(DataWarehouse, df_seoulpark_fin, 'THEME_EVENT')

    # 어린이대공원 데이터 DW에 저장
    @classmethod
    def __save_childpark_data(cls, df_childpark):
        childpark_list = df_childpark.collect()
        df_childpark_fin = cls.__create_df_with_eventdata(childpark_num, childpark_list)
        df_childpark_fin = df_childpark_fin.select(col('THEME_NUM'), to_date(col('STD_DATE'), 'yyyy-MM-dd').alias('STD_DATE'),
                                                col('EVENT_OX'), col('EVENT_NAME'))                                             
        save_data(DataWarehouse, df_childpark_fin, 'THEME_EVENT')

    # 롯데월드 데이터 DW에 저장
    @classmethod
    def __save_lotteworld_data(cls, df_lotteworld):
        lotteworld_list = df_lotteworld.collect()
        df_lotteworld_fin = cls.__create_df_with_eventdata(lotteworld_num, lotteworld_list)
        df_lotteworld_fin = df_lotteworld_fin.select(col('THEME_NUM'), to_date(col('STD_DATE'), 'yyyy-MM-dd').alias('STD_DATE'),
                                                col('EVENT_OX'), col('EVENT_NAME'))
        save_data(DataWarehouse, df_lotteworld_fin, 'THEME_EVENT')

    # 에버랜드 데이터 DW에 저장
    @classmethod
    def __save_everland_data(cls, df_everland):
        everland_list = df_everland.collect()
        df_everland_fin = cls.__create_df_with_eventdata(everland_num, everland_list)
        df_everland_fin = df_everland_fin.select(col('THEME_NUM'), to_date(col('STD_DATE'), 'yyyy-MM-dd').alias('STD_DATE'),
                                                col('EVENT_OX'), col('EVENT_NAME'))
        save_data(DataWarehouse, df_everland_fin, 'THEME_EVENT')

    # HDFS에서 데이터 가져와 데이터프레임으로 생성
    @classmethod
    def __get_data_from_hdfs(cls):
        everland_file_name = cls.FILE_DIR + 'everland/' + 'everland_event_2018_2022.csv'
        seoulpark_file_name = cls.FILE_DIR + 'seoulpark/' + 'event_seoulpark_2017_202206.csv'
        lotteworld_file_name = cls.FILE_DIR + 'lotteworld/' + 'lotteworld_event_2018_2022.csv'
        childpark_file_name = cls.FILE_DIR + 'childpark/' + 'event_childpark_2017_202206.csv'

        df_everland = get_spark_session().read.csv(everland_file_name, encoding='CP949', header=True)
        df_seoulpark = get_spark_session().read.csv(seoulpark_file_name, encoding='CP949', header=True)
        df_lotteworld = get_spark_session().read.csv(lotteworld_file_name, encoding='CP949', header=True)
        df_childpark = get_spark_session().read.csv(childpark_file_name, encoding='CP949', header=True)
        return df_everland,df_seoulpark,df_lotteworld,df_childpark


    # db에서 테마파크 번호 가져오기
    @classmethod
    def __get_theme_num(cls):
        df_themepark = find_data(DataWarehouse, "THEMEPARK")
        df_themepark.show()

        everland_num = df_themepark.where(col('THEME_NAME') == '에버랜드').first()[0]
        lotteworld_num = df_themepark.where(col('THEME_NAME') == '롯데월드').first()[0]
        seoulpark_num = df_themepark.where(col('THEME_NAME') == '서울대공원').first()[0]
        childpark_num = df_themepark.where(col('THEME_NAME') == '서울어린이대공원').first()[0]

    # 데이터 가공
    @classmethod
    def __create_df_with_eventdata(cls, theme_num, events_data):
        data = []
        for i in range(2118, 111, -1):  # 1753, 111, -1   / 2118, 111, -1
            tmp_dict = {}
            day = cal_std_day2(i)

            tmp_dict['THEME_NUM'] = int(theme_num)
            tmp_dict['STD_DATE'] = cls.__create_date(day[:4], day[4:6], day[6:8])

            for k in range(len(events_data)):
                startdate = str(events_data[k][1])
                enddate = str(events_data[k][2])
                date1 = dt.datetime(int(startdate[:4]), int(startdate[4:6]), int(startdate[6:8]))
                date2 = dt.datetime(int(enddate[:4]), int(enddate[4:6]), int(enddate[6:8]))
                d = dt.datetime(int(day[:4]), int(day[4:6]), int(day[6:8]))
                if date1 <= d <= date2:
                    tmp_dict['EVENT_OX'] = 1
                    tmp_dict['EVENT_NAME'] = events_data[k][0]
                    break
            else:
                tmp_dict['EVENT_OX'] = 0
                tmp_dict['EVENT_NAME'] = ''

            data.append(tmp_dict)

        df_fin = get_spark_session().createDataFrame(data)
        return df_fin

    # 날짜 형식 변환(YYYY-MM-dd 형태)
    @classmethod
    def __create_date(cls, year, month, day):
        if len(month) < 2:
            month = '0' + str(month)
        if len(day) < 2:
            day = '0' + str(day)
        res = year + '-' + month + '-' + day
        return res