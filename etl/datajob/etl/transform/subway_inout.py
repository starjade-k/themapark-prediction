from pyspark.sql.functions import col
from infra.jdbc import DataWarehouse, find_data, save_data
from infra.spark_session import get_spark_session
from infra.util import cal_std_day2


class SubwayInOutTransformer:
    FILE_DIR = '/theme_park/subway/'

    @classmethod
    def transform(cls):
        df_themepark = find_data(DataWarehouse, "THEMEPARK")
        #df_themepark.show()

        # db에서 테마파크 번호 가져오기
        seoulpark_num = df_themepark.where(col('THEME_NAME') == '서울대공원').first()[0]
        childpark_num = df_themepark.where(col('THEME_NAME') == '서울어린이대공원').first()[0]

        file_name = cls.FILE_DIR + 'subway_inout_' + cal_std_day2(4) + '.csv'
        df_sbw = get_spark_session().read.csv(file_name, header=True, encoding='cp949')
        sbw_list = df_sbw.collect()

        data = []
        for row in sbw_list:
            tmp_dict = {}
            tmp_date = row['날짜']
            tmp_dict['STD_DATE'] = tmp_date[:4] + '-' + tmp_date[4:6] + '-' + tmp_date[6:8]
            sbw_nm = row['역명']
            if sbw_nm in ('아차산(어린이대공원후문)', '어린이대공원(세종대)'):
                for tmp in data:
                    if tmp['THEME_NUM'] == int(childpark_num):
                        tmp['IN_NUM'] += int(row['승차 승객수'])
                        tmp['OUT_NUM'] += int(row['하차 승객수'])
                        break
                else:
                    tmp_dict['THEME_NUM'] = int(childpark_num)
                    tmp_dict['IN_NUM'] = int(row['승차 승객수'])
                    tmp_dict['OUT_NUM'] = int(row['하차 승객수'])
                    data.append(tmp_dict)
            elif sbw_nm == '대공원':
                tmp_dict['THEME_NUM'] = int(seoulpark_num)
                tmp_dict['IN_NUM'] = int(row['승차 승객수'])
                tmp_dict['OUT_NUM'] = int(row['하차 승객수'])
                data.append(tmp_dict)

        df_fin = get_spark_session().createDataFrame(data)
        df_fin = df_fin.withColumn('STD_DATE', col('STD_DATE').cast('date'))
        save_data(DataWarehouse, df_fin, 'SUBWAY_INOUT')

