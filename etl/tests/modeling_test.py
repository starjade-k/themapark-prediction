import unittest
from datajob.modeling.childpark import ChildParkModeling
from datajob.modeling.sbw_out_predict import SbwOutPredict
from datajob.modeling.navi_predict import NaviPredict

# test command : python3 -W ignore -m unittest tests.modeling_test.MTest.test1
class MTest(unittest.TestCase):

    def test1(self):
        ChildParkModeling.exec()
    
    def test2(self):
        SbwOutPredict.exec('서울어린이대공원')

    def test3(self):
        NaviPredict.exec('서울어린이대공원')

    
if __name__ == "__main__":
    """ This is executed when run from the command line """
    unittest.main()  