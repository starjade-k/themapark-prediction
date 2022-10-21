import unittest
from datajob.etl.transform.transform_dust import DustTransformer

from datajob.etl.transform.transform_weather import WeatherTransformer



class MTest(unittest.TestCase):

    def test1(self):
        WeatherTransformer.transform()

    def test2(self):
        DustTransformer.transform()




if __name__ == "__main__":
    """ This is executed when run from the command line """
    unittest.main()  