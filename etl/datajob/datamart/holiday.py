from datetime import date
from pyspark.sql.functions import col
from infra.jdbc import DataMart, DataWarehouse, overwrite_trunc_data, save_data
from infra.spark_session import get_spark_session
from infra.util import cal_std_day_after, cal_std_day_after2

class Holiday:
    FILE_DIR = '/theme_park/holiday/'
    @classmethod
    def save(cls, after_cnt=7):
        # HDFS에서 데이터 가져오기
        holidays = cls.__get_data_from_hdfs(after_cnt)

        data = []

        # 데이터프레임 이용해 데이터 가공
        cls.__create_df_data(after_cnt, holidays, data)
        
        # DM에 저장
        cls.__save_to_DM(data)

    @classmethod
    def __save_to_DM(cls, data):
        df_fin = get_spark_session().createDataFrame(data)
        df_fin = df_fin.withColumn('STD_DATE', col('STD_DATE').cast('date'))
        overwrite_trunc_data(DataMart, df_fin, 'PRE_HOLIDAY')

    @classmethod
    def __create_df_data(cls, after_cnt, holidays, data):
        for i in range(after_cnt):
            tmp_dict = {}
            tmp_dict['STD_DATE'] = cal_std_day_after2(i)

            tmp_date = cal_std_day_after(i)
            
            tmp_date2 = date(int(tmp_date[:4]), int(tmp_date[4:6]), int(tmp_date[6:8]))
            weekday = tmp_date2.weekday()
            if weekday in (5, 6):
                tmp_dict['HOLIDAY_OX'] = 1
            else:
                for holiday in holidays:
                    start_date = holiday['시작날짜']
                    end_date = holiday['종료날짜']
                    if tmp_date >= start_date and tmp_date <= end_date:
                        tmp_dict['HOLIDAY_OX'] = 1
                        break
                else:
                    tmp_dict['HOLIDAY_OX'] = 0

            data.append(tmp_dict)

    @classmethod
    def __get_data_from_hdfs(cls, after_cnt):
        file_name = cls.FILE_DIR + 'holiday_' + cal_std_day_after(0) + '_' + cal_std_day_after(after_cnt-1) + '.csv'
        df_hol = get_spark_session().read.csv(file_name, encoding='CP949', header=True)
        holidays = df_hol.collect()
        return holidays