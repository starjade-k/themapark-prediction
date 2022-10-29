import unittest
from datajob.etl.transform.child_parking import ChildparkingTransformer
from datajob.etl.transform.child_price import ChildpriceTransformer
from datajob.etl.transform.child_weather import ChildweatherTransformer
from datajob.etl.transform.ever_price import EverpriceTransformer
from datajob.etl.transform.lotte_price import LottepriceTransformer
from datajob.etl.transform.pre_air_weather import PreairweatherTransformer
from datajob.etl.transform.pre_weather import PreweatherTransformer
from datajob.etl.transform.seoul_corona import SeoulcoronaTransformer
from datajob.etl.transform.seoul_parking import SeoulparkingTransformer
from datajob.etl.transform.seoul_price import SeoulpriceTransformer
from datajob.etl.transform.seoul_weather import SeoulweatherTransformer
from datajob.etl.transform.transform_child import ChildTransformer
from datajob.etl.transform.today_dust import TodustTransformer
from datajob.etl.transform.transform_seoul import SeoulTransformer
from datajob.etl.transform.transform_subway import SubwayTransformer
from datajob.etl.transform.today_weather import ToweatherTransformer



class MTest(unittest.TestCase):

    def test1(self):
        ToweatherTransformer.transform()

    def test2(self):
        TodustTransformer.transform()

    # def test3(self):
    #     PreweatherTransformer.transform()

    def test4(self):
        PreairweatherTransformer.transform()
    

    def test5(self):
        SubwayTransformer.transform()

    def test6(self):
        ChildTransformer.transform()

    def test7(self):
        SeoulTransformer.transform()       

    def test8(self):
        SeoulpriceTransformer.transform()    

    def test9(self):
        ChildpriceTransformer.transform()

    def test10(self):
        LottepriceTransformer.transform()

    def test11(self):
        EverpriceTransformer.transform()

    def test12(self):
        SeoulparkingTransformer.transform()

    def test13(self):
        ChildparkingTransformer.transform()

    def test14(self):
        SeoulcoronaTransformer.transform()

    def test15(self):
        ChildweatherTransformer.transform()

    def test16(self):
        SeoulweatherTransformer.transform()            
if __name__ == "__main__":
    """ This is executed when run from the command line """
    unittest.main()  