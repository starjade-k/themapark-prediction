import json
import bs4
import pandas as pd
from infra.hdfs_client import get_client
from infra.logger import get_logger
from infra.util import cal_std_day2, cal_std_day_after, execute_rest_api


class EventSeoulParkExtractor:
    BASE_URL = 'https://grandpark.seoul.go.kr/munhwa/munhwaList/ko/S001005001004.do'
    DETAIL_URL = 'https://grandpark.seoul.go.kr/munhwa/munhwaView/ko/S001005001004.do'
    FILE_DIR = '/theme_park/event/seoulpark/'

    @classmethod
    def extract_data(cls, after_cnt=7):
        base_params = {
            'pageIndex': '1',
            'searchgubun': '',
            'searchWord': ''
        }
        detail_params = {
            'pageIndex': '1',
            'mh_no': '46121',
            'searchgubun': '',
            'searchWord': ''
        }
        log_dict_base = cls.__create_log_dict(base_params)
        page_nums = cls.__get_event_pagenum(base_params, log_dict_base)
        
        log_dict_detail = cls.__create_log_dict(detail_params)
        try:
            df = cls.__get_event_data(detail_params, page_nums)
            print(df)
            file_name = cls.FILE_DIR + 'event_seoulpark_' + cal_std_day2(0) + '_' + cal_std_day_after(after_cnt-1) + '.csv'
            #file_name = cls.FILE_DIR + 'event_seoulpark_2017_202206.csv'
            with get_client().write(file_name, overwrite=True, encoding='cp949') as writer:
                df.to_csv(writer, header=['행사명', '시작날짜', '종료날짜'], index=False)
        except Exception as e:
            cls.__dump_log(log_dict_detail, e)

    # 각 행사 페이지에서 행사명과 날짜 가져옴
    @classmethod
    def __get_event_data(cls, detail_params, page_nums):
        seoulpark = set()
        for i in range(len(page_nums)):
            detail_params['mh_no'] = page_nums[i]
            response = execute_rest_api('get', cls.DETAIL_URL, {}, detail_params)
            bs_obj = bs4.BeautifulSoup(response.text, 'html.parser')
            title = bs_obj.find('div', {'class': 'view-header'}).find('h5').text.replace('\t', '').replace('\r\n', '')
            tmp_date = bs_obj.find('div', {'class': 'view-header'}).find('li').text.replace('\t', '').replace('\r\n', '')
            tmp_date = tmp_date.split(' ')
            start_date = tmp_date[1].replace('.', '')
            end_date = tmp_date[3].replace('.', '')
            res = (title, start_date, end_date)
            seoulpark.add(res)
        df = pd.DataFrame(list(seoulpark))
        return df

    # 각 행사들의 페이지 번호 가져옴
    @classmethod
    def __get_event_pagenum(cls, base_params, log_dict_base):
        mores = []
        mh_nos = []
        try:
            for i in range(1, 2):
                base_params['pageIndex'] = str(i)
                response = execute_rest_api('get', cls.BASE_URL, {}, base_params)
                bs_obj = bs4.BeautifulSoup(response.text, 'html.parser')
                mores += bs_obj.findAll('a', {'class': 'more-button'})
            for more in mores:
                mh_nos.append(more['onclick'].split("'")[3])
        except Exception as e:
            cls.__dump_log(log_dict_base, e)
        return mh_nos

    # 로그 dump
    @classmethod
    def __dump_log(cls, log_dict, e):
        log_dict['err_msg'] = e.__str__()
        log_json = json.dumps(log_dict, ensure_ascii=False)
        print(log_dict['err_msg'])
        get_logger('event_seoulpark_extract').error(log_json)

    # 로그데이터 생성
    @classmethod
    def __create_log_dict(cls, params):
        log_dict = {
                "is_success": "Fail",
                "type": "event_seoulpark_extract",
                "params": params
            }
        return log_dict