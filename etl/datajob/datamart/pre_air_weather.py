from datetime import date, datetime
from pyspark.sql.types import *
from pyspark.sql.functions import *
import datetime as dt
from infra.jdbc import DataWarehouse, DataMart, find_data, overwrite_data, overwrite_trunc_data, save_data
from infra.spark_session import get_spark_session
from infra.util import cal_std_day

class PreAirWeather:

    @classmethod
    def save(cls):
        weather = find_data(DataMart, 'DAILY_WEATHER')
        dust = find_data(DataMart, 'DAILY_AIR')
        wd_data = weather.join(dust, (weather.STD_DATE == dust.STD_DATE) & (weather.THEME_NUM == dust.THEME_NUM) )\
                        .select(weather.STD_DATE,weather.THEME_NUM,'HIGH_TEMP','LOW_TEMP','DIFF_TEMP','RAIN_AMOUNT','AVG_WIND','HIGH_WIND',dust.PM10,dust.PM25)

        # DM에 저장
        overwrite_trunc_data(DataMart, wd_data, 'PRE_AIR_WEATHER')