import json
import pandas as pd
import bs4
from infra.hdfs_client import get_client
from infra.util import cal_std_day2, cal_std_day_after, execute_rest_api
from infra.logger import get_logger


class EverlandInfoExtractor:
    FILE_DIR = '/theme_park/info/everland/'
    URL = 'https://www.everland.com/service/front/frontTime.do'

    @classmethod
    def extract_data(cls, after_cnt=7):
        cls.__get_operation_time(after_cnt)

        cls.__get_holiday_facility(after_cnt)


    # 에버랜드 운휴시설 크롤링
    @classmethod
    def __get_holiday_facility(cls, after_cnt):
        # 운휴시설 파라미터
        params_hol = {
            'method': 'holidayRslt',
            'siteCode': 'CT00101',
            'baseDate': '20221026'
        }
        # bs이용해 데이터 가져온 후 가공 후, 데이터프레임 생성
        for i in range(0, after_cnt):
            try:
                # 크롤링 위한 파라미터 설정 후 데이터 크롤링
                params_hol['baseDate'] = cal_std_day_after(i)
                log_dict = cls.__create_log_dict(params_hol)
                response = execute_rest_api('post', cls.URL, {}, params=params_hol)

                # bs이용해 데이터 가공 후, 데이터프레임 생성
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

                # 데이터프레임 데이터를 CSV파일로 HDFS에 저장
                file_name = cls.FILE_DIR + 'holiday_area_everland_' + params_hol['baseDate'] + '.csv'
                with get_client().write(file_name, overwrite=True, encoding='cp949') as writer:
                    df.to_csv(writer, header=['운휴시설'], index=False)
            except Exception as e:
                cls.__dump_log(log_dict, e)

    # 에버랜드 운영시간 크롤링
    @classmethod
    def __get_operation_time(cls, after_cnt):
        # 파라미터 설정
        params_time = {
            'method': 'operTimeRslt',
            'siteCode': 'CT00101',
            'baseDate': '20221026'
        }

        # bs이용해 데이터 가져온 후 가공 후, 데이터프레임 생성
        for i in range(0, after_cnt):
            try:
                # 크롤링 위한 파라미터 설정 후 데이터 크롤링
                params_time['baseDate'] = cal_std_day_after(i)
                log_dict = cls.__create_log_dict(params_time)
                response = execute_rest_api('get', cls.URL, {}, params=params_time)

                # bs이용해 데이터 가공
                bs_obj = bs4.BeautifulSoup(response.text, 'html.parser')
                op_time = bs_obj.find('p', {'class': 'usetime'}).find('strong').text.split(' ~ ')
                df = pd.DataFrame(dict({'시작시간': [op_time[0]], '종료시간': [op_time[1]]}))
                print(df)

                # 데이터프레임 데이터를 CSV파일로 HDFS에 저장
                file_name = cls.FILE_DIR + 'time_everland_' + params_time['baseDate'] + '.csv'
                with get_client().write(file_name, overwrite=True, encoding='cp949') as writer:
                    df.to_csv(writer, header=['시작시간', '종료시간'], index=False)
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