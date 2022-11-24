import datetime as dt
from pyspark.sql.functions import col, to_date
from infra.jdbc import DataWarehouse, find_data, save_data
from infra.spark_session import get_spark_session
from infra.util import cal_std_day2, cal_std_day_after


class ThemeParkEventTransformer:
    FILE_DIR = '/theme_park/event/'
    @classmethod
    def transform(cls, after_cnt=7):
        childpark_num, seoulpark_num = cls.__get_theme_num()

        themeparks = [('childpark', childpark_num), 
                        ('seoulpark', seoulpark_num)]

        for themepark in themeparks:
            df_fin = cls.__parse_and_get_df(themepark[0], themepark[1], after_cnt)
            df_fin.show()
            # DW에 저장
            save_data(DataWarehouse, df_fin, "THEME_EVENT")

    # DW에서 테마파크 번호 가져오기
    @classmethod
    def __get_theme_num(cls):
        df_themepark = find_data(DataWarehouse, "THEMEPARK")

        childpark_num = df_themepark.where(col('THEME_NAME') == '서울어린이대공원').first()[0]
        seoulpark_num = df_themepark.where(col('THEME_NAME') == '서울대공원').first()[0]
        return childpark_num,seoulpark_num

    # 데이터 가져온 후, 데이터 가공해 데이터 프레임 생성
    @classmethod
    def __parse_and_get_df(cls, themepark, themepark_num, after_cnt):
        df_event = cls.__get_data_from_hdfs(themepark, after_cnt)
        event_list = df_event.collect()
        df_fin = cls.__create_df_with_eventdata(themepark_num, event_list)
        df_fin = df_fin.select(col('THEME_NUM'), to_date(col('STD_DATE'), 'yyyy-MM-dd').alias('STD_DATE'),
                                col('EVENT_OX'), col('EVENT_NAME'))          
        return df_fin

    # HDFS에서 데이터 가져와 데이터프레임으로 생성
    @classmethod
    def __get_data_from_hdfs(cls, themepark, after_cnt):
        file_name = cls.FILE_DIR + themepark + '/event_' + themepark + '_' + cal_std_day2(0) + '_' + cal_std_day_after(after_cnt-1) + '.csv'
        df_event = get_spark_session().read.csv(file_name, encoding='CP949', header=True)
        return df_event

    # 데이터 가공
    @classmethod
    def __create_df_with_eventdata(cls, theme_num, events_data):
        data = []
        for i in range(0, 1):  # 오늘날짜만
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