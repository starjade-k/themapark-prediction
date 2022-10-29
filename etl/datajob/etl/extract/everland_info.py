import json
import pandas as pd
import bs4
from infra.hdfs_client import get_client
from infra.util import cal_std_day2, execute_rest_api
from infra.logger import get_logger


class EverlandInfoExtractor:
    FILE_DIR = '/theme_park/info/everland/'
    URL = 'https://www.everland.com/service/front/frontTime.do'

    @classmethod
    def extract_data(cls):
        # ㅡㅡㅡㅡㅡㅡ 에버랜드 운영시간 ㅡㅡㅡㅡㅡㅡ
        params_time = {
            'method': 'operTimeRslt',
            'siteCode': 'CT00101',
            'baseDate': '20221026'
        }
        log_dict = cls.__create_log_dict(params_time)
        try:
            params_time['baseDate'] = cal_std_day2(0)
            response = execute_rest_api('get', cls.URL, {}, params=params_time)
            bs_obj = bs4.BeautifulSoup(response.text, 'html.parser')
            op_time = bs_obj.find('p', {'class': 'usetime'}).find('strong').text.split(' ~ ')
            df = pd.DataFrame(dict({'시작시간': [op_time[0]], '종료시간': [op_time[1]]}))
            print(df)
            file_name = cls.FILE_DIR + 'time_everland_' + cal_std_day2(0) + '.csv'
            with get_client().write(file_name, overwrite=True, encoding='cp949') as writer:
                df.to_csv(writer, header=['시작시간', '종료시간'], index=False)
        except Exception as e:
            cls.__dump_log(log_dict, e)


        # ㅡㅡㅡㅡㅡㅡ 에버랜드 운휴시설 ㅡㅡㅡㅡㅡㅡ
        params_hol = {
            'method': 'holidayRslt',
            'siteCode': 'CT00101',
            'baseDate': '20221026'
        }
        params_hol['baseDate'] = cal_std_day2(0)
        log_dict = cls.__create_log_dict(params_hol)
        try:
            response = execute_rest_api('post', cls.URL, {}, params=params_hol)
            bs_obj = bs4.BeautifulSoup(response.text, 'html.parser')
            land_names = ['매직랜드', '주토피아', '유러피언 어드벤처', '아메리칸 어드벤처 / 글로벌 페어']

            data = []
            for i, land_name in enumerate(land_names):
                table = bs_obj.find('table', {'summary': land_name})
                attr_info = table.findAll('td')[2:]
                for k in range(0, len(attr_info), 2):
                    if attr_info[k+1].text == 'CLOSED':
                        data.append(attr_info[k].text)
            df = pd.DataFrame(data)
            print(df)
            file_name = cls.FILE_DIR + 'holiday_area_everland_' + cal_std_day2(0) + '.csv'
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
        get_logger('everland_info_extract').error(log_json)

    # 로그데이터 생성
    @classmethod
    def __create_log_dict(cls, params):
        log_dict = {
                "is_success": "Fail",
                "type": "everland_info_extract",
                "params": params
            }
        return log_dict