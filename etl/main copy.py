import sys
from datajob.datamart.pre_air_weather import PreAirWeather
from datajob.datamart.today_weather import TodayWeather
from datajob.etl.extract.pre_dust import PredustExtractor
from datajob.etl.extract.pre_weather import PreweatherExtractor
from datajob.etl.extract.today_dust import TodustExtractor
from datajob.etl.extract.today_weather import ToweatherExtractor
from datajob.etl.transform.pre_air_weather import PreairweatherTransformer
from datajob.etl.transform.pre_weather import PreweatherTransformer
from datajob.etl.transform.today_dust import TodustTransformer
from datajob.etl.transform.today_weather import ToweatherTransformer
from datajob.datamart.pre_themepark_event import PreThemeParkEvent
from datajob.datamart.themepark_hol_fac import ThemeparkHolFac
from datajob.datamart.themepark_time import ThemeparkTime
from datajob.etl.extract.event_childpark import EventChildParkExtractor
from datajob.etl.extract.event_seoulpark import EventSeoulParkExtractor
from datajob.etl.extract.everland_info import EverlandInfoExtractor
from datajob.etl.extract.lotteworld_info import LotteworldInfoExtractor
from datajob.etl.extract.navi_search import NaviSearchExtractor
from datajob.etl.transform.navi_search import NaviSearchTransformer
from datajob.etl.transform.transform_event import ThemeParkEventTransformer


def transfrom_execute():
    ToweatherTransformer.transform()
    TodustTransformer.transform()
    PreweatherTransformer.transform()
    PreairweatherTransformer.transform()

def datamart_execute():
    TodayWeather.save()
    PreAirWeather.save()

works = {
    'extract':{
        'today_weather': ToweatherExtractor.extract_data
        ,'today_dust':TodustExtractor.extract_data
        ,'pre_weather': PreweatherExtractor.extract_data
        ,'pre_dust':PredustExtractor.extract_data
    }
    ,'transform':{
        'execute':transfrom_execute
        ,'today_weather':ToweatherTransformer.transform
        ,'today_dust':TodustTransformer.transform
        ,'pre_weather': PreweatherTransformer.transform
        ,'pre_air_weather':PreairweatherTransformer.transform
    }
    ,'datamart':{
        'execute':datamart_execute
        ,'today_weather':TodayWeather.save
        ,'pre_air_weather':PreAirWeather.save



def transfrom_execute():
    ThemeParkEventTransformer.transform()
    NaviSearchTransformer.transform()

def datamart_execute():
    PreThemeParkEvent.save()
    ThemeparkTime.save()
    ThemeparkHolFac.save()

works = {
    'extract':{
        'navi_search': NaviSearchExtractor.extract_data
        ,'event_childpark': EventChildParkExtractor.extract_data
        ,'event_seoulpark': EventSeoulParkExtractor.extract_data
        , 'everland_info' : EverlandInfoExtractor.extract_data
        , 'lotteworld_info' : LotteworldInfoExtractor.extract_data
    }
    ,'transform':{
        'execute': transfrom_execute
        ,'transform_event': ThemeParkEventTransformer.transform
        ,'navi_search': NaviSearchTransformer.transform
    }
    ,'datamart':{
        'execute': datamart_execute
        ,'pre_themepark_event': PreThemeParkEvent.save
        ,'themepark_time' : ThemeparkTime.save
        ,'themepark_hol_fac' : ThemeparkHolFac.save
    }
}

if __name__ == "__main__":
    args = sys.argv
    print(args)

    # python3 main.py extract event_childpark
    # main.py 작업(extract, transform, datamart) 저장할 위치(테이블)
    # 매개변수 2개
    if len(args) != 3:
        raise Exception('2개의 전달인자가 필요합니다.')

    if args[1] not in works.keys():
        raise Exception('첫번째 전달인자가 이상함 >> ' + str(works.keys()))

    if args[2] not in works[args[1]].keys():
        raise Exception('두번째 전달인자가 이상함 >> ' + str(works[args[1]].keys()))

    work = works[args[1]][args[2]]
    work()
  