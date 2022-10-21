import unittest
from datajob.etl.transform.navi_search import NaviSearchTransformer
from datajob.etl.transform.past_airdata import PastAirDataTransformer
from datajob.etl.transform.themepark_event import ThemeParkEventTransformer


class MTest(unittest.TestCase):

    def test1(self):
        NaviSearchTransformer.transform()

    def test2(self):
        ThemeParkEventTransformer.transform()

    def test3(self):
        PastAirDataTransformer.transform()



if __name__ == "__main__":
    """ This is executed when run from the command line """
    unittest.main()  