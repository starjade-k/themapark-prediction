from datetime import datetime
import json
from urllib import response
import requests
from bs4 import BeautifulSoup
from infra.util import cal_std_day, execute_rest_api
from infra.hdfs_client import get_client
from infra.logger import get_logger
import time

class PredustExtractor:
    file_dir = '/themapark/dust/'
    file_name = 'pre_dust' + cal_std_day(0) + '.json'
    
    @classmethod
    def extract_data(cls):
        data=[]
        base_url=['4129000000','1171000000','4146100000','1121500000']
        cols=['지역','날짜','미세먼지','초미세먼지']
        rows_list = []
        for l in base_url:
            url = 'https://www.kr-weathernews.com/mv3/if/pm.fcgi?region={}'.format(l)
            response = requests.get(url)
            res = response.json()
            rows = []
            day = cal_std_day(0)

            #지역
            if l == '4129000000':
                rows.append('1')
            elif l =='1171000000':
                rows.append('3')
            elif l =='4146100000':
                rows.append('4')
            elif l =='1121500000':
                rows.append('2')        
            #날짜
            rows.append(day)
            #미세먼지
            rows.append(res['pm']['history'][-1]['pm10'])
            #초미세먼지
            rows.append(res['pm']['history'][-1]['pm25'])
            rows_list.append(rows)
            
            for i in range(0, 7):
                rows = []
                #지역
                if l == '4129000000':
                    rows.append('1')
                elif l =='1171000000':
                    rows.append('3')
                elif l =='4146100000':
                    rows.append('4')
                elif l =='1121500000':
                    rows.append('2') 
                #날짜
                rows.append(str(res['pm']['forcast']['daily'][i]['year']) +'-'+ str(res['pm']['forcast']['daily'][i]['mon']) +'-' + str(res['pm']['forcast']['daily'][i]['day']))
                #미세먼지
                rows.append(res['pm']['forcast']['daily'][i]['pm10'])
                #초미세먼지
                rows.append(res['pm']['forcast']['daily'][i]['pm25'])
                rows_list.append(rows)
                
        for rows in rows_list:
            tmp=dict(zip(cols,rows))
            data.append(tmp)
            
        result = {
            'meta':{
                'desc':'미세먼지',
                'cols':{
                    '지역':'지역',
                    '날짜':'날짜',
                    '미세먼지':'미세먼지',
                    '초미세먼지':'초미세먼지'
                },
            },
        'data':data
        }
        get_client().write(cls.file_dir+cls.file_name, json.dumps(result, ensure_ascii=False), encoding='utf-8',overwrite=True)