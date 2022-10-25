import unittest
from datajob.etl.extract.event_seoulpark import EventSeoulParkExtractor
from datajob.etl.transform.past_navi_search import PastNaviSearchTransformer
from datajob.etl.transform.past_airdata import PastAirDataTransformer
from datajob.etl.transform.past_themepark_event import PastThemeParkEventTransformer
from datajob.etl.transform.transform_event import ThemeParkEventTransformer
from datajob.etl.transform.transform_event_childpark import EventChildParkTransformer
from datajob.etl.transform.transform_event_seoulpark import EventSeoulParkTransformer


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