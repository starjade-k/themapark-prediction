import unittest
from datajob.datamart.co_popu_density import CoPopuDensity
from datajob.datamart.co_vaccine import CoVaccine
from datajob.etl.extract.corona_api import CoronaApiExtractor
from datajob.etl.extract.corona_vaccine import CoronaVaccineExtractor
from datajob.etl.transform.corona_patient import CoronaPatientTransformer
from datajob.etl.transform.corona_vaccine import CoronaVaccineTransformer
from datajob.etl.transform.loc import LocTransformer


class MTest(unittest.TestCase):

    def test1(self):
        CoPopuDensity.save()

    def test2(self):
        CoVaccine.save()
    



if __name__ == "__main__":
    """ This is executed when run from the command line """
    unittest.main()  