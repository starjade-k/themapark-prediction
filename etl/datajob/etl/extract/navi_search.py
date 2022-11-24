import json
import requests
import pandas as pd
from infra.hdfs_client import get_client
from infra.util import cal_std_day2, execute_rest_api
from infra.logger import get_logger


class NaviSearchExtractor:
    URL = 'https://datalab.visitkorea.or.kr/visualize/getTempleteData.do'
    FILE_DIR = '/theme_park/navigation/'

    @classmethod
    def extract_data(cls, before_cnt=2):
        # 크롤링 위한 파라미터 설정
        params = {
            'txtSGG_CD': '1',
            'txtSIDO_ARR': '',
            'SGG_CD': '98',
            'TMAP_CATE_MCLS_CD':'문화관광',
            'SIDO_ARR': '',
            'BASE_YM1': '20181211',
            'BASE_YM2': '20181211',
            'srchAreaDate': '5',
            'qid': 'BDT_03_04_002'
        }
        log_dict = cls.__create_log_dict(params)
        data = {'날짜': [], '에버랜드': [], '서울대공원': [], '서울어린이대공원': [], '롯데월드': []}

        try:
            df = cls.__get_nav_data(params, data, before_cnt)
            print(df)

            # 데이터프레임 데이터를 CSV파일로 HDFS에 저장
            file_name = cls.FILE_DIR + 'navi_search_' + params['BASE_YM1'] + '.csv'
            with get_client().write(file_name, overwrite=True, encoding='cp949') as writer:
                df.to_csv(writer, header=['날짜', '에버랜드', '서울대공원',  '서울어린이대공원', '롯데월드'], index=False)
        except Exception as e:
            cls.__dump_log(log_dict, e)

    # 네비게이션 데이터 크롤링
    @classmethod
    def __get_nav_data(cls, params, data, before_cnt):
        # 데이터 가져온 후 가공 후, 데이터프레임 생성
        for i in range(before_cnt, before_cnt + 1):
            # 크롤링 위한 파라미터 설정 후 데이터 크롤링
            day = cal_std_day2(i)
            revised_day = cls.__create_date(day[:4], day[4:6], day[6:8])
            data['날짜'].append(revised_day)
            params['BASE_YM1'] = day
            params['BASE_YM2'] = day
            response = execute_rest_api('post', cls.URL, {}, params)

            # 데이터 가공
            res = response.json()
            for tmp in res['list']:
                if tmp['ITS_BRO_NM'] == '에버랜드':
                    data['에버랜드'].append(tmp['SRCH_CNT'])
                elif tmp['ITS_BRO_NM'] == '서울대공원':
                    data['서울대공원'].append(tmp['SRCH_CNT'])
                elif tmp['ITS_BRO_NM'] == '어린이대공원':
                    data['서울어린이대공원'].append(tmp['SRCH_CNT'])
                elif tmp['ITS_BRO_NM'] == '롯데월드잠실점':
                    data['롯데월드'].append(tmp['SRCH_CNT'])
        df = pd.DataFrame(data)
        return df

    # 로그 dump
    @classmethod
    def __dump_log(cls, log_dict, e):
        log_dict['err_msg'] = e.__str__()
        log_json = json.dumps(log_dict, ensure_ascii=False)
        print(log_dict['err_msg'])
        get_logger('navi_search_extract').error(log_json)

    # 로그데이터 생성
    @classmethod
    def __create_log_dict(cls, params):
        log_dict = {
                "is_success": "Fail",
                "type": "navi_search_extract",
                "std_day": params['BASE_YM1'],
                "params": params
            }
        return log_dict

    # 날짜 변환 함수
    @classmethod
    def __create_date(cls, year, month, day):
        if len(month) < 2:
            month = '0' + str(month)
        if len(day) < 2:
            day = '0' + str(day)
        res = year + '-' + month + '-' + day
        return res