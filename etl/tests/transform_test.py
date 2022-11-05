import unittest
from datajob.etl.extract.event_seoulpark import EventSeoulParkExtractor
from datajob.etl.transform.ever_lotte_entrance import EverLotteEntrance
from datajob.etl.transform.holiday import HolidayTransformer
from datajob.etl.transform.navi_search import NaviSearchTransformer
from datajob.etl.transform.past_airdata import PastAirDataTransformer
from datajob.etl.transform.past_themepark_event import PastThemeParkEventTransformer
from datajob.etl.transform.pre_childpark import PreChildParkTransformer
from datajob.etl.transform.pre_seoulpark import PreSeoulParkTransformer
from datajob.etl.transform.subway_inout import SubwayInOutTransformer
from datajob.etl.transform.transform_event import ThemeParkEventTransformer


# python3 -W ignore -m unittest tests.transform_test.MTest.test1
class MTest(unittest.TestCase):

    def test1(self):
        NaviSearchTransformer.transform()

    def test2(self):
        PastThemeParkEventTransformer.transform()

    def test3(self):
        PastAirDataTransformer.transform()

    def test4(self):
        ThemeParkEventTransformer.transform()
    
    def test5(self):
        EverLotteEntrance.transform()

    def test6(self):
        PreSeoulParkTransformer.transform()

    def test7(self):
        HolidayTransformer.transform()

    def test8(self):
        PreChildParkTransformer.transform()

    def test9(self):
        SubwayInOutTransformer.transform()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    unittest.main()  