import unittest
from datajob.etl.extract.extract_dust import DustExtractor
from datajob.etl.extract.extract_weather import WeatherExtractor


class MTest(unittest.TestCase):

    def test1(self):
        WeatherExtractor.extract_data()

    def test2(self):
        DustExtractor.extract_data()



if __name__ == "__main__":
    """ This is executed when run from the command line """
    unittest.main()    