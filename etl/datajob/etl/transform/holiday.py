from datetime import date
from pyspark.sql.functions import col
from infra.jdbc import DataWarehouse, save_data
from infra.spark_session import get_spark_session
from infra.util import cal_std_day2, cal_std_day

class HolidayTransformer:
    FILE_DIR = '/theme_park/holiday/'
    @classmethod
    def transform(cls):
        df_hol = get_spark_session().read.csv(cls.FILE_DIR + 'holiday_201801_202206.csv', encoding='CP949', header=True)
        holidays = df_hol.collect()

        data = []

        for i in range(1765, 123, -1):  # 1765 , 123, -1
            tmp_dict = {}
            tmp_dict['STD_DATE'] = cal_std_day(i)

            tmp_date = cal_std_day2(i)
            
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
        
        df_fin = get_spark_session().createDataFrame(data)
        df_fin = df_fin.withColumn('STD_DATE', col('STD_DATE').cast('date'))
        save_data(DataWarehouse, df_fin, 'HOLIDAY')

            
            