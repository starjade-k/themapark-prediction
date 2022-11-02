import unittest
from datajob.datamart.ever_lotte_entrance import LotteEverEntrance
from datajob.datamart.holiday import Holiday
from datajob.datamart.pre_themepark_event import PreThemeParkEvent
from datajob.operation.themepark_hol_fac import ThemeparkHolFac
from datajob.operation.themepark_time import ThemeparkTime

# test command : python3 -W ignore -m unittest tests.dm_test.MTest.test1
class MTest(unittest.TestCase):

    def test1(self):
        PreThemeParkEvent.save()

    def test2(self):
        ThemeparkTime.save()

    def test3(self):
        ThemeparkHolFac.save()

    def test4(self):
        LotteEverEntrance.save()

    def test5(self):
        Holiday.save()

    

if __name__ == "__main__":
    """ This is executed when run from the command line """
    unittest.main()  