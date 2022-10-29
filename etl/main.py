import sys
from datajob.datamart.pre_air_weather import PreAirWeather
from datajob.datamart.today_weather import TodayWeather
from datajob.etl.extract.pre_dust import PredustExtractor
from datajob.etl.extract.pre_weather import PreweatherExtractor
from datajob.etl.extract.today_dust import TodustExtractor
from datajob.etl.extract.today_weather import ToweatherExtractor
from datajob.etl.transform.pre_air_weather import PreairweatherTransformer, PredustTransformer
from datajob.etl.transform.pre_weather import PreweatherTransformer
from datajob.etl.transform.today_dust import TodustTransformer
from datajob.etl.transform.today_weather import ToweatherTransformer


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
    }
}

if __name__ == "__main__":
    args = sys.argv
    print(args)

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
  
