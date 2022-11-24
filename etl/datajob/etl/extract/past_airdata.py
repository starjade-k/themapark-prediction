import pandas as pd
from infra.hdfs_client import get_client
from infra.util import cal_std_day2, cal_std_month, execute_rest_api


# 131201_별양동_경기 과천시 코오롱로 53 문원초등학교_199422_435759

class PastAirDataExtractor:
    URL = 'https://www.airkorea.or.kr/web/pollution/getPastChart'
    FILE_DIR = '/theme_park/past_weather/'
    STATION_CODE = ['111141', '111273', '131414', '131201', '132112']  # 광진구(어린이대공원), 송파구(롯데월드), 용인시(에버랜드), 과천시(서울대공원), 춘천(레고랜드)
    STATION_NAME = ['gwangjin', 'songpa', 'yongin', 'gwacheon', 'chuncheon']

    gwangjin_202206_pm10 = [23, 29, 38, 31, 24, 6, 5, 14, 24, 24, 22, 21, 22, 12, 10, 15, 33, 23, 26, 32, 32, 27, 41, 21, 46, 23, 13, 17, 15, 5]
    gwangjin_202206_pm25 = [9, 16, 23, 18, 15, 2, 2, 8, 13, 15, 10, 13, 13, 4, 5, 8, 20, 12, 15, 19, 19, 15, 25, 14, 33, 13, 5, 6, 7, 2]

    songpa_202206_pm10 = [25, 31, 42, 38, 26, 8, 7, 16, 27, 31, 25, 22, 26, 15, 9, 19, 34, 25, 22, 29, 34, 31, 32, 23, 46, 22, 13, 16, 14, 7]
    songpa_202206_pm25 = [10, 15, 24, 20, 15, 3, 3, 9, 15, 18, 14, 15, 15, 5, 4, 9, 22, 14, 11, 15, 19, 17, 17, 16, 33, 12, 5, 6, 7, 4]

    yongin_202206_pm10 = [27, 34, 40, 38, 21, 13, 8, 15, 28, 31, 21, 21, 26, 12, 12, 14, 31, 23, 22, 35, 38, 36, 26, 16, 38, 23, 13, 13, 10, 5]
    yongin_202206_pm25 = [8, 14, 20, 19, 10, 3, 2, 7, 15, 16, 11, 11, 12, 3, 3, 9, 18, 12, 11, 20, 23, 20, 16, 10, 25, 11, 3, 3, 2, 2]

    gwacheon_202206_pm10 = [21, 27, 40, 34, 23, 10, 8, 19, 22, 28, 25, 22, 27, 15, 12, 17, 33, 23, 24, 25, 30, 31, 25, 17, 54, 19, 12, 16, 11, 6]
    gwacheon_202206_pm25 = [8, 14, 19, 15, 11, 4, 4, 10, 11, 15, 12, 13, 13, 4, 8, 7, 17, 10, 11, 12, 11, 14, 15, 11, 28, 9, 4, 4, 4, 2]

    chuncheon_202206_pm10 = [26, 28, 27, 27, 21, 5, 7, 30, 15, 25, 27, 15, 12, 13, 9, 16, 33, 32, 27, 28, 32, 31, 27, 15, 36, 21, 13, 12, 10, 6]
    chuncheon_202206_pm25 = [7, 11, 10, 10, 9, 2, 2, 3, 6, 9, 7, 6, 4, 3, 2, 6, 16, 17, 13, 13, 16, 15, 14, 5, 21, 9, 4, 3, 4, 2]

    @classmethod
    def extract_data(cls):
        params = {
            'dateDiv': '일간',
            'period': '202203',
            'stationCode': '111141'  # 111273
        }

        for i in range(len(cls.STATION_CODE)):
            data = cls.__parse_air_data(params, cls.STATION_CODE[i])

            data = cls.__append_202206_data(data, cls.STATION_NAME[i])
        
            df = pd.DataFrame(list(set(data)), columns=['STD_DATE', 'PM10', 'PM25'])
            df = df.sort_values(by=['STD_DATE'])  # 날짜순으로 정렬
            print(df)

            # 데이터프레임 데이터를 CSV파일로 HDFS에 저장
            file_name = cls.FILE_DIR + cls.STATION_NAME[i] + '_air_2017_202206.csv'
            with get_client().write(file_name, overwrite=True, encoding='cp949') as writer:
                df.to_csv(writer, header=['STD_DATE', 'PM10', 'PM25'], index=False)


    # 2022년 6월 데이터 수동으로 추가
    @classmethod
    def __append_202206_data(cls, data, station):
        loc_pm10 = []
        loc_pm25 = []
        if station == 'gwangjin':
            loc_pm10 = cls.gwangjin_202206_pm10
            loc_pm25 = cls.gwangjin_202206_pm25
        elif station == 'songpa':
            loc_pm10 = cls.songpa_202206_pm10
            loc_pm25 = cls.songpa_202206_pm25
        elif station == 'yongin':
            loc_pm10 = cls.yongin_202206_pm10
            loc_pm25 = cls.yongin_202206_pm25            
        elif station == 'gwacheon':
            loc_pm10 = cls.gwacheon_202206_pm10
            loc_pm25 = cls.gwacheon_202206_pm25    
        elif station == 'chuncheon':
            loc_pm10 = cls.chuncheon_202206_pm10
            loc_pm25 = cls.chuncheon_202206_pm25    

        k = 0
        for i in range(146, 116, -1):  # 20220601 ~ 20220630
            tmp_date = cal_std_day2(i)
            date = cls.__create_date(tmp_date[:4], tmp_date[4:6], tmp_date[6:8])
            tmp_data = (date, loc_pm10[k], loc_pm25[k])
            data.append(tmp_data)
            k += 1
        return data

    # 웹에서 크롤링한다음 데이터 저장
    @classmethod
    def __parse_air_data(cls, params, station):
        data = []

        for i in range(70, 4, -1):   # 201701 ~ 202205
            # 크롤링 위한 파라미터 설정 후 데이터 크롤링
            params['period'] = cal_std_month(i)
            params['stationCode'] = station
            response = execute_rest_api('get', cls.URL, {}, params)

            # 데이터 가공
            res = response.json()
            charts = res['charts']
            for i, chart in enumerate(charts):
                tmp_date = chart['DATA_TIME'].replace('-', '')
                date = cls.__create_date(tmp_date[:4], tmp_date[4:6], tmp_date[6:8])
                pm10 = chart['VALUE_10007']
                pm25 = chart['VALUE_10008']
                if pm10 is None:        # 결측치 보정
                    pm10 = data[-1][1]
                if pm25 is None:
                    pm25 = data[-1][2]
                tmp_data = (date, pm10, pm25)
                data.append(tmp_data)
        return data

    # 날짜데이터를 YYYY-MM-dd 형태로 변환
    @classmethod
    def __create_date(cls, year, month, day):
        if len(month) < 2:
            month = '0' + str(month)
        if len(day) < 2:
            day = '0' + str(day)
        res = year + '-' + month + '-' + day
        return res