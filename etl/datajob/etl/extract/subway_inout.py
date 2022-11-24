import bs4
import pandas as pd
from infra.hdfs_client import get_client
from infra.util import cal_std_day2, execute_rest_api

class SubwayInOutExtractor:
    SERVICE_KEY = '4745776c5065756e3332734a4a4368'
    BASE_URL = 'http://openapi.seoul.go.kr:8088/'
    DETAIL_URL = '/xml/CardSubwayStatsNew/1/500/'
    FILE_DIR = '/theme_park/subway/'

    @classmethod
    def extract_data(cls):
        # 크롤링 위한 파라미터 설정 후 데이터 크롤링
        url = cls.BASE_URL + cls.SERVICE_KEY + cls.DETAIL_URL + cal_std_day2(4)
        response = execute_rest_api('get', url, {}, {})

        # bs이용해 데이터 가공 후, 데이터프레임 생성
        bs_obj = bs4.BeautifulSoup(response.text, "html.parser")
        data = []
        rows = list(bs_obj.findAll("row"))
        for row in rows:
            station_nm = row.find('sub_sta_nm').text
            if station_nm in ('아차산(어린이대공원후문)', '어린이대공원(세종대)', '대공원'):    
                dt = row.find('use_dt').text
                in_num = row.find('ride_pasgr_num').text
                out_num = row.find('alight_pasgr_num').text
                tmp_dict = {'날짜': dt, '역명': station_nm, '승차 승객수': in_num, '하차 승객수': out_num}
                data.append(tmp_dict)

        # 데이터프레임 데이터를 CSV파일로 HDFS에 저장
        df = pd.DataFrame(data)
        print(df)
        file_name = cls.FILE_DIR + 'subway_inout_' + cal_std_day2(4) + '.csv'
        with get_client().write(file_name, overwrite=True, encoding='cp949') as writer:
            df.to_csv(writer, header=['날짜', '역명', '승차 승객수', '하차 승객수'], index=False)
