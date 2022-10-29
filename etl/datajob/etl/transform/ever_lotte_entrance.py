from pyspark.sql.functions import col
from infra.jdbc import DataWarehouse, find_data, save_data
from infra.spark_session import get_spark_session

class EverLotteEntrance:
    FILE_DIR = '/theme_park/entrance/'
    MONTH_DICT = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
                'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    @classmethod
    def transform(cls):
        df_themepark = find_data(DataWarehouse, "THEMEPARK")
        df_themepark.show()

        # db에서 테마파크 번호 가져오기
        everland_num = df_themepark.where(col('THEME_NAME') == '에버랜드').first()[0]
        lotteworld_num = df_themepark.where(col('THEME_NAME') == '롯데월드').first()[0]

        # hdfs에서 파일 읽어오기
        df = get_spark_session().read.csv(cls.FILE_DIR + 'everland_lotteworld_monthly_entrance.csv', encoding='CP949', header=True)
        raw_data = df.collect()
        data = []

        # Transform 진행
        for row in raw_data:
            tmp_date = cls.__transform_date(row['해당연월'])
            if not (row['에버랜드'] is None):
                tmp_ever_dict = {'THEME_NUM': int(everland_num), 'STD_DATE': tmp_date, 'ENT_NUM': int(row['에버랜드'])}
                data.append(tmp_ever_dict)
            if not (row['롯데월드'] is None):
                tmp_lotte_dict = {'THEME_NUM': int(lotteworld_num), 'STD_DATE': tmp_date, 'ENT_NUM': int(row['롯데월드'])}
                data.append(tmp_lotte_dict)

        df_fin = get_spark_session().createDataFrame(data)
        df_fin.show(10)
        save_data(DataWarehouse, df_fin, "THEME_ENTRANCE2")

    @classmethod
    def __transform_date(cls, date):
        date_split = date.split('-')
        month_befor = date_split[0]
        year_befor = date_split[1]
        month_after = cls.MONTH_DICT[month_befor]
        year_after = '20' + year_befor
        return year_after + '-' + month_after