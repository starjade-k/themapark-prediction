import json
import bs4
import pandas as pd
from infra.hdfs_client import get_client
from infra.util import cal_std_day2, execute_rest_api
from infra.logger import get_logger


class LotteworldInfoExtractor:
    FILE_DIR = '/theme_park/info/lotteworld/'
    TIME_URL = 'https://adventure.lotteworld.com/kor/main/index.do'
    HOL_URL = 'https://adventure.lotteworld.com/kor/usage-guide/service/index.do'

    @classmethod
    def extract_data(cls):
        # ㅡㅡㅡㅡㅡㅡ 롯데월드 운영시간 ㅡㅡㅡㅡㅡㅡ
        log_dict = cls.__create_log_dict({})
        try:
            response = execute_rest_api('get', cls.TIME_URL, {}, {})
            bs_obj = bs4.BeautifulSoup(response.text, 'html.parser')
            op_time = bs_obj.find('div', {'class': 'mainTodayArea'}).find('p', {'class': 'txt'}).text.strip().split(' - ')
            df = pd.DataFrame(dict({'시작시간': [op_time[0]], '종료시간': [op_time[1]]}))
            print(df)
            file_name = cls.FILE_DIR + 'time_lotteworld_' + cal_std_day2(0) + '.csv'
            with get_client().write(file_name, overwrite=True, encoding='cp949') as writer:
                df.to_csv(writer, header=['시작시간', '종료시간'], index=False)
        except Exception as e:
            cls.__dump_log(log_dict, e)

        # ㅡㅡㅡㅡㅡㅡ 롯데월드 운휴시설 ㅡㅡㅡㅡㅡㅡ
        params_fac = {
            'oprtDt': '20221026'
        }
        params_fac['oprtDt'] = cal_std_day2(0)
        log_dict = cls.__create_log_dict(params_fac)
        try:
            response = execute_rest_api('get', cls.HOL_URL, {}, params=params_fac)
            bs_obj = bs4.BeautifulSoup(response.text, 'html.parser')
            holiday_list = bs_obj.find('div', {'class': 'holidayArea'}).findAll('p', {'class': 'txt'})
            holiday_area_list = []
            for holiday in holiday_list:
                holiday_area_list.append(holiday.text)
            df = pd.DataFrame(holiday_area_list)
            print(df)
            file_name = cls.FILE_DIR + 'holiday_area_lotteworld_' + cal_std_day2(0) + '.csv'
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

