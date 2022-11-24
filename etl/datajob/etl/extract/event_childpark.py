import json
import bs4
import pandas as pd
from infra.hdfs_client import get_client
from infra.logger import get_logger
from infra.util import cal_std_day2, cal_std_day_after, execute_rest_api


class EventChildParkExtractor:
    URL = 'https://www.sisul.or.kr/open_content/sub/schedule/detail.do'
    FILE_DIR = '/theme_park/event/childpark/'

    @classmethod
    def extract_data(cls, after_cnt=7):
        # 파라미터 설정
        params = {
            'year': '2018',
            'month': '04',
            'day': '18',
            'site_div': 'childrenpark'
        }
        log_dict = cls.__create_log_dict(params)
        childrenpark = set()
        try:
            # 행사정보 데이터 크롤링한 다음 데이터프레임 생성
            df = cls.__get_event_data(after_cnt, params, childrenpark)
            print(df)

            # 데이터프레임 데이터를 CSV파일로 HDFS에 저장
            file_name = cls.FILE_DIR + 'event_childpark_' + cal_std_day2(0) + '_' + cal_std_day_after(after_cnt-1) + '.csv'
            with get_client().write(file_name, overwrite=True, encoding='cp949') as writer:
                df.to_csv(writer, header=['행사명', '시작날짜', '종료날짜'], index=False)
        except Exception as e:
            cls.__dump_log(log_dict, e)

    # 행사정보 데이터 크롤링
    @classmethod
    def __get_event_data(cls, after_cnt, params, childrenpark):
        # bs이용해 데이터 가져온 후 가공 후, 데이터프레임 생성
        for i in range(0, after_cnt):
            # 크롤링 위한 파라미터 설정 후 데이터 크롤링
            tmp_date = cal_std_day_after(i)
            params['year'] = tmp_date[:4]
            params['month'] = tmp_date[4:6]
            params['day'] = tmp_date[6:8]
            response = execute_rest_api('post', cls.URL, {}, params)
            
            # bs이용해 데이터 가공 후, 데이터프레임 생성
            bs_obj = bs4.BeautifulSoup(response.text, 'html.parser')
            tits = bs_obj.findAll('p', {'class': 'tit'})
            for tit in tits:
                tmp = tit.text.strip().replace('\r\n', '').replace('\t', '')
                print(tmp)
                if tmp != '선택한 일의 일정이 없습니다.':
                    tmp_date_list = tmp[:25][1:-1].split(' ~ ')
                    start_date = tmp_date_list[0].replace('.', '')
                    end_date = tmp_date_list[1].replace('.', '')
                    title = tmp[25:]
                    res = (title, start_date, end_date)
                    childrenpark.add(res)
        df = pd.DataFrame(list(childrenpark))
        return df

    # 로그 dump
    @classmethod
    def __dump_log(cls, log_dict, e):
        log_dict['err_msg'] = e.__str__()
        log_json = json.dumps(log_dict, ensure_ascii=False)
        print(log_dict['err_msg'])
        get_logger('event_childpark_extract').error(log_json)

    # 로그데이터 생성
    @classmethod
    def __create_log_dict(cls, params):
        log_dict = {
                "is_success": "Fail",
                "type": "event_childpark_extract",
                "params": params
            }
        return log_dict