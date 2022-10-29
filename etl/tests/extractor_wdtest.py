import unittest
from datajob.etl.extract.pre_dust import PredustExtractor
from datajob.etl.extract.pre_weather import PreweatherExtractor
from datajob.etl.extract.today_dust import TodustExtractor
from datajob.etl.extract.today_weather import ToweatherExtractor


class MTest(unittest.TestCase):

    def test1(self):
        ToweatherExtractor.extract_data()

    def test2(self):
        TodustExtractor.extract_data()

    def test3(self):
        PredustExtractor.extract_data()

    def test4(self):
        PreweatherExtractor.extract_data()
    



if __name__ == "__main__":
    """ This is executed when run from the command line """
    unittest.main()    