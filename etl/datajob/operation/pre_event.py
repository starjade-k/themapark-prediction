import datetime as dt
from pyspark.sql.functions import col, to_date
from infra.jdbc import OperationDB, DataWarehouse, find_data, overwrite_trunc_data
from infra.spark_session import get_spark_session
from infra.util import cal_std_day2, cal_std_day_after


class PreEvent:
    FILE_DIR = '/theme_park/event/'
    @classmethod
    def save(cls, after_cnt=7):
        themeparks = [('childpark', '서울어린이대공원'), 
                        ('seoulpark', '서울대공원')]

        df_childpark = cls.__parse_and_get_df(themeparks[0][0], themeparks[0][1], after_cnt)
        df_seoulpark = cls.__parse_and_get_df(themeparks[1][0], themeparks[1][1], after_cnt)

        # 서울대공원, 어린이대공원 union
        df_fin = df_childpark.union(df_seoulpark)
        df_fin = df_fin.select(col('THEME_NAME'), to_date(col('STD_DATE'), 'yyyy-MM-dd').alias('STD_DATE'),
                                col('EVENT_OX'), col('EVENT_NAME'))
        df_fin.show()

        # DM에 쓰기
        overwrite_trunc_data(OperationDB, df_fin, "PRE_EVENT")

    @classmethod
    def __parse_and_get_df(cls, themepark, themepark_num, after_cnt):
        file_name = cls.FILE_DIR + themepark + '/event_' + themepark + '_' + cal_std_day2(0) + '_' + cal_std_day_after(after_cnt-1) + '.csv'
        df_event = get_spark_session().read.csv(file_name, encoding='CP949', header=True)
        event_list = df_event.collect()
        df_fin = cls.__create_df_with_eventdata(themepark_num, event_list, after_cnt)
        return df_fin

    @classmethod
    def __create_df_with_eventdata(cls, theme_name, events_data, after_cnt):
        data = []
        for i in range(0, after_cnt):  # 오늘날짜 포함 7일치
            tmp_dict = {}
            day = cal_std_day_after(i)

            tmp_dict['THEME_NAME'] = theme_name
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

    @classmethod
    def __create_date(cls, year, month, day):
        if len(month) < 2:
            month = '0' + str(month)
        if len(day) < 2:
            day = '0' + str(day)
        res = year + '-' + month + '-' + day
        return res