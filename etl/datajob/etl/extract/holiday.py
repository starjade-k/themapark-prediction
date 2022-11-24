import bs4
import pandas as pd
from infra.hdfs_client import get_client
from infra.util import cal_std_day, cal_std_day2, cal_std_day_after, cal_std_month, execute_rest_api

class HolidayExtractor:
    FILE_DIR = '/theme_park/holiday/'
    URL = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getHoliDeInfo'
    SERVICE_KEY = 'i0nVQiQVStPAvJl1sDmfbDQprcQJy6u9WTTZ8GCG0te6Px4VkQLxrgDA97OBTJlcV6o/teMff1c5RDNOrrQr8Q=='

    @classmethod
    def extract_data(cls, after_cnt=7):
        params = {'ServiceKey': cls.SERVICE_KEY, 'solYear': '2022', 'solMonth': '10'}

        data = set()
        for i in range(after_cnt):
            date = cal_std_day_after(i)
            year = date[:4]
            month = date[4:6]
            day = date[6:8]

            # 파라미터 설정 후, api 호출
            params['solYear'] = year
            params['solMonth'] = month
            response = execute_rest_api('get', cls.URL, {}, params=params)

            # bs이용해 데이터 가공
            if response.status_code:
                bs_obj = bs4.BeautifulSoup(response.text, 'xml')
                names = []
                locdates = []
                for n in bs_obj.findAll('dateName'):
                    names.append(n.text)
                for l in bs_obj.findAll('locdate'):
                    locdates.append(l.text)
                
                tmp_dict = {}
                for name, date in zip(names, locdates):
                    if name in tmp_dict.keys():
                        tmp_dict[name].append(date)
                    else:
                        tmp_dict[name] = [date]
                
                # 대체공휴일 날짜 가공
                for name, value in tmp_dict.items():
                    if name == '대체공휴일':
                        for i in range(len(value)):
                            data.add((name, value[i], value[i]))
                    else:
                        data.add((name, value[0], value[-1]))


        # 데이터프레임 데이터를 CSV파일로 HDFS에 저장
        df = pd.DataFrame(list(data))
        file_name = cls.FILE_DIR + 'holiday_' + cal_std_day_after(0) + '_' + cal_std_day_after(after_cnt-1) + '.csv'
        if len(data) == 0:
            get_client().write(file_name, data=data, overwrite=True, encoding='cp949')
        else:
            with get_client().write(file_name, overwrite=True, encoding='cp949') as writer:
                df.to_csv(writer, header=['공휴일명', '시작날짜', '종료날짜'], index=False)