import json
import requests
from bs4 import BeautifulSoup
from infra.util import cal_std_day
from infra.hdfs_client import get_client
from pyspark.sql.types import *

class PreweatherExtractor:
    file_dir = '/themapark/weather/'
    file_name = 'pre_weather' + cal_std_day(0) + '.json'
    
    @classmethod
    def extract_data(cls):
        data = []
        cols =['지역','날짜','최고기온','최저기온','일교차','강수량','바람','최대풍속','img']
        ld = ['0201010202','0203020106','0101010000','0101010000 ']

        for n in ld:
            url = 'http://www.weatheri.co.kr/forecast/forecast01.php?rid={}&k=1&a_name=용인'.format(n)
            response = requests.get(url)
            html = response.content.decode('utf-8','replace')
            soup = BeautifulSoup(html, 'html.parser')
            date = soup.findAll('td',{'bgcolor':'#EBF1DE'})
            temhigh = soup.findAll('font',{'color':'#FF0000'})
            temlow = soup.findAll('font',{'color':'blue'})
            rw = soup.findAll('font',{'color':'7F7F7F'})
            topwind = soup.findAll('font',{'color':'#7F7F7F'})
            weather_img = soup.findAll('img',{'border':'0'})
            
            #일자 별 풍속 리스트 생성
            wind_top1 =[]
            wind_top2 =[]
            wind_top3 =[]
            wind_top4 =[]
            wind_top5 =[]
            wind_top6 =[]
            wind_top7 =[]
            wind_top8 =[]
            wind_top9 =[]
            wind_top10 =[]
            # 일자 별로 시간 별 풍속 리스트에 넣기
            for w in range(0,7):
                wind_top1.append(topwind[1:9][w].text.strip())
                wind_top2.append(topwind[19:27][w].text.strip())
                wind_top3.append(topwind[37:45][w].text.strip())
                wind_top4.append(topwind[55:63][w].text.strip())
                wind_top5.append(topwind[73:81][w].text.strip())
                wind_top6.append(topwind[91:99][w].text.strip())
                wind_top7.append(topwind[109:117][w].text.strip())
                wind_top8.append(topwind[127:135][w].text.strip())
                wind_top9.append(topwind[145:153][w].text.strip())
                wind_top10.append(topwind[163:171][w].text.strip())

            for i in range(0, 7):
                rows=[]
                if n == '0201010202':
                    rows.append('1')
                elif n == '0203020106':
                    rows.append('4')
                elif n == '0101010000':
                    rows.append('3')
                elif n == '0101010000 ':
                    rows.append('2')        
                #날짜 0~9
                rows.append('2022-' + date[i].text.replace(' ','').replace('월','-').replace('일','').split('(')[0])
                #최고기온 0~9
                rows.append(float(temhigh[i].text.replace('˚C','')))
                #최저기온 0~9
                rows.append(float(temlow[i].text.replace('˚C','')))
                #일교차
                rows.append(float(temhigh[i].text.replace('˚C','')) - float(temlow[i].text.replace('˚C','')))
                #풍속,강수량,일교차,날씨이미지
                if i==0:
                    day1_img = 'http://www.weatheri.co.kr/' + weather_img[6].get('src').replace('../../','')
                    rows.append(float(rw[1].text.replace(' mm','').replace('-','0')))
                    rows.append(float(rw[0].text.replace(' m/s','').replace('-','0')))
                    rows.append(float(max(wind_top1)))
                    rows.append(day1_img)
                elif i==1:
                    day2_img = 'http://www.weatheri.co.kr/' + weather_img[7].get('src').replace('../../','')
                    rows.append(float(rw[3].text.replace(' mm','').replace('-','0')))
                    rows.append(float(rw[2].text.replace(' m/s','').replace('-','0')))
                    rows.append(float(max(wind_top2)))
                    rows.append(day2_img)
                elif i==2:
                    day3_img = 'http://www.weatheri.co.kr/' + weather_img[8].get('src').replace('../../','')
                    rows.append(float(rw[5].text.replace(' mm','').replace('-','0')))
                    rows.append(float(rw[4].text.replace(' m/s','').replace('-','0')))
                    rows.append(float(max(wind_top3)))
                    rows.append(day3_img)
                elif i==3:
                    day4_img = 'http://www.weatheri.co.kr/' + weather_img[9].get('src').replace('../../','')
                    rows.append(float(rw[7].text.replace(' mm','').replace('-','0')))
                    rows.append(float(rw[6].text.replace(' m/s','').replace('-','0')))
                    rows.append(float(max(wind_top4)))
                    rows.append(day4_img)
                elif i==4:
                    day5_img = 'http://www.weatheri.co.kr/' + weather_img[10].get('src').replace('../../','')
                    rows.append(float(rw[9].text.replace(' mm','').replace('-','0')))
                    rows.append(float(rw[8].text.replace(' m/s','').replace('-','0')))
                    rows.append(float(max(wind_top5)))
                    rows.append(day5_img)
                elif i==5:
                    day6_img = 'http://www.weatheri.co.kr/' + weather_img[11].get('src').replace('../../','')
                    rows.append(float(rw[11].text.replace(' mm','').replace('-','0')))
                    rows.append(float(rw[10].text.replace(' m/s','').replace('-','0')))
                    rows.append(float(max(wind_top6)))
                    rows.append(day6_img)
                elif i==6:
                    day7_img = 'http://www.weatheri.co.kr/' + weather_img[12].get('src').replace('../../','')
                    rows.append(float(rw[13].text.replace(' mm','').replace('-','0')))
                    rows.append(float(rw[12].text.replace(' m/s','').replace('-','0')))
                    rows.append(float(max(wind_top7)))
                    rows.append(day7_img)
                elif i==7:
                    rows.append(float(rw[15].text.replace(' mm','').replace('-','0')))
                    rows.append(float(rw[14].text.replace(' m/s','').replace('-','0')))
                    rows.append(float(max(wind_top8)))
                elif i==8:
                    rows.append(float(rw[17].text.replace(' mm','').replace('-','0')))
                    rows.append(float(rw[16].text.replace(' m/s','').replace('-','0')))
                    rows.append(float(max(wind_top9)))
                elif i==9:
                    rows.append(float(rw[19].text.replace(' mm','').replace('-','0')))
                    rows.append(float(rw[18].text.replace(' m/s','').replace('-','0')))
                    rows.append(float(max(wind_top10)))
                tmp=dict(zip(cols,rows))
                data.append(tmp)    
                
                
        res = {
            'meta':{
                'desc':'날씨예보',
                'cols':{
                    '지역':'지역',
                    '날짜':'날짜',
                    '최고기온':'최고기온',
                    '최저기온':'최저기온',
                    '일교차':'일교차',
                    '강수량':'강수량',
                    '바람':'바람',
                    '최대풍속':'최대풍속',
                    'img' : 'img'
                },
            },
        'data':data
        }

        get_client().write(cls.file_dir+cls.file_name, json.dumps(res, ensure_ascii=False), encoding='utf-8',overwrite=True)