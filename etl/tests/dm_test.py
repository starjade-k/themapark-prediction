import unittest
from datajob.datamart.pre_air_weather import PreAirWeather
from datajob.datamart.today_weather import TodayWeather



class MTest(unittest.TestCase):

    def test1(self):
        TodayWeather.save()

    def test2(self):
        PreAirWeather.save()
    



if __name__ == "__main__":
    """ This is executed when run from the command line """
    unittest.main()  