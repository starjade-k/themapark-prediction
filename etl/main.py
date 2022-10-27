import sys
from datajob.datamart.pre_themepark_event import PreThemeParkEvent
from datajob.datamart.themepark_hol_fac import ThemeparkHolFac
from datajob.datamart.themepark_time import ThemeparkTime
from datajob.etl.extract.event_childpark import EventChildParkExtractor
from datajob.etl.extract.event_seoulpark import EventSeoulParkExtractor
from datajob.etl.extract.everland_info import EverlandInfoExtractor
from datajob.etl.extract.lotteworld_info import LotteworldInfoExtractor
from datajob.etl.transform.transform_event import ThemeParkEventTransformer


def transfrom_execute():
    ThemeParkEventTransformer.transform()

def datamart_execute():
    PreThemeParkEvent.save()
    ThemeparkTime.save()
    ThemeparkHolFac.save()

works = {
    'extract':{
        'event_childpark': EventChildParkExtractor.extract_data
        ,'event_seoulpark': EventSeoulParkExtractor.extract_data
        , 'everland_info' : EverlandInfoExtractor.extract_data
        , 'lotteworld_info' : LotteworldInfoExtractor.extract_data
    }
    ,'transform':{
        'execute': transfrom_execute
        ,'transform_event': ThemeParkEventTransformer.transform
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
  
