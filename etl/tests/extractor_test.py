import unittest
from datajob.etl.extract.event_childpark import EventChildParkExtractor
from datajob.etl.extract.event_seoulpark import EventSeoulParkExtractor
from datajob.etl.extract.everland_info import EverlandInfoExtractor
from datajob.etl.extract.lotteworld_info import LotteworldInfoExtractor
from datajob.etl.extract.past_navi_search import NaviSearchExtractor
from datajob.etl.extract.past_airdata import PastAirDataExtractor

# test command : python3 -W ignore -m unittest tests.extractor_test.MTest.test1
class MTest(unittest.TestCase):

    def test1(self):
        NaviSearchExtractor.extract_data()

    def test2(self):
        EventChildParkExtractor.extract_data()

    def test3(self):
        EventSeoulParkExtractor.extract_data()
    
    def test4(self):
        PastAirDataExtractor.extract_data()

    def test5(self):
        LotteworldInfoExtractor.extract_data()

    def test6(self):
        EverlandInfoExtractor.extract_data()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    unittest.main()    