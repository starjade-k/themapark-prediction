import unittest
from datajob.etl.extract.corona_api import CoronaApiExtractor
from datajob.etl.extract.corona_vaccine import CoronaVaccineExtractor
from datajob.etl.transform.corona_patient import CoronaPatientTransformer
from datajob.etl.transform.corona_vaccine import CoronaVaccineTransformer
from datajob.etl.transform.loc import LocTransformer
from datajob.etl.transform.navi_search import NaviSearchTransformer
from datajob.etl.transform.themepark_event import ThemeParkEventTransformer


class MTest(unittest.TestCase):

    def test1(self):
        NaviSearchTransformer.transform()

    def test2(self):
        ThemeParkEventTransformer.transform()

    def test3(self):
        LocTransformer.transform()



if __name__ == "__main__":
    """ This is executed when run from the command line """
    unittest.main()  