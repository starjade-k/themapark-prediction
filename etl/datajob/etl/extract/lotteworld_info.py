import json
import bs4
import pandas as pd
from infra.hdfs_client import get_client
from infra.util import cal_std_day2, cal_std_day_after, execute_rest_api
from infra.logger import get_logger


class LotteworldInfoExtractor:
    FILE_DIR = '/theme_park/info/lotteworld/'
    URL = 'https://adventure.lotteworld.com/kor/usage-guide/service/index.do'

    @classmethod
    def extract_data(cls, after_cnt=7):
        params = cls.__get_operation_time(after_cnt)
        cls.__get_holiday_facility(after_cnt, params)
        

    # 롯데월드 운영시간 크롤링
    @classmethod
    def __get_operation_time(cls, after_cnt):
        params = {
            'oprtDt': '20221026'
        }
        # bs이용해 데이터 가져온 후 가공 후, 데이터프레임 생성
        for i in range(0, after_cnt):
            try:
                # 크롤링 위한 파라미터 설정 후 데이터 크롤링
                params['oprtDt'] = cal_std_day_after(i)
                log_dict = cls.__create_log_dict(params)
                response = execute_rest_api('get', cls.URL, {}, params=params)

                # bs이용해 데이터 가공 후, 데이터프레임 생성
                bs_obj = bs4.BeautifulSoup(response.text, 'html.parser')
                time_area = bs_obj.find('div', {'class': 'timeVisArea'})
                start_time = time_area['data-strt-si'] + ':' + time_area['data-strt-mi']
                end_time = time_area['data-end-si'] + ':' + time_area['data-end-mi']

                # 데이터프레임 데이터를 CSV파일로 HDFS에 저장
                df = pd.DataFrame({'시작시간': [start_time], '종료시간': [end_time]})
                print(df)
                file_name = cls.FILE_DIR + 'time_lotteworld_' + params['oprtDt'] + '.csv'
                with get_client().write(file_name, overwrite=True, encoding='cp949') as writer:
                    df.to_csv(writer, header=['시작시간', '종료시간'], index=False)
            except Exception as e:
                cls.__dump_log(log_dict, e)
        return params


    # 롯데월드 운휴시설 크롤링
    @classmethod
    def __get_holiday_facility(cls, after_cnt, params):
        # bs이용해 데이터 가져온 후 가공 후, 데이터프레임 생성
        for i in range(0, after_cnt):
            try:
                # 크롤링 위한 파라미터 설정 후 데이터 크롤링
                params['oprtDt'] = cal_std_day_after(i)
                log_dict = cls.__create_log_dict(params)
                response = execute_rest_api('get', cls.URL, {}, params=params)

                # bs이용해 데이터 가공 후, 데이터프레임 생성
                bs_obj = bs4.BeautifulSoup(response.text, 'html.parser')
                holiday_list = bs_obj.find('div', {'class': 'holidayArea'}).findAll('p', {'class': 'txt'})
                holiday_area_list = []
                for holiday in holiday_list:
                    holiday_area_list.append(holiday.text)

                # 데이터프레임 데이터를 CSV파일로 HDFS에 저장
                df = pd.DataFrame(holiday_area_list)
                print(df)
                file_name = cls.FILE_DIR + 'holiday_area_lotteworld_' + params['oprtDt'] + '.csv'
                with get_client().write(file_name, overwrite=True, encoding='cp949') as writer:
                    df.to_csv(writer, header=['운휴시설'], index=False)
            except Exception as e:
                cls.__dump_log(log_dict, e)
            

    # 로그 dump
    @classmethod
    def __dump_log(cls, log_dict, e):
        log_dict['err_msg'] = e.__str__()
        log_json = json.dumps(log_dict, ensure_ascii=False)
        print(log_dict['err_msg'])
        get_logger('lotteworld_info_extract').error(log_json)

    # 로그데이터 생성
    @classmethod
    def __create_log_dict(cls, params):
        log_dict = {
                "is_success": "Fail",
                "type": "lotteworld_info_extract",
                "params": params
            }
        return log_dict

