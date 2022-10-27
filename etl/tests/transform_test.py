import unittest
from datajob.etl.extract.event_seoulpark import EventSeoulParkExtractor
from datajob.etl.transform.past_navi_search import PastNaviSearchTransformer
from datajob.etl.transform.past_airdata import PastAirDataTransformer
from datajob.etl.transform.past_themepark_event import PastThemeParkEventTransformer
from datajob.etl.transform.transform_event import ThemeParkEventTransformer


# python3 -W ignore -m unittest tests.transform_test.MTest.test1
class MTest(unittest.TestCase):

    def test1(self):
        PastNaviSearchTransformer.transform()

    def test2(self):
        PastThemeParkEventTransformer.transform()

    def test3(self):
        PastAirDataTransformer.transform()

    def test4(self):
        ThemeParkEventTransformer.transform()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    unittest.main()  