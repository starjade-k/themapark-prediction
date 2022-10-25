import unittest

from datajob.datamart.pre_themepark_event import PreThemeParkEvent

# test command : python3 -W ignore -m unittest tests.dm_test.MTest.test1
class MTest(unittest.TestCase):

    def test1(self):
        PreThemeParkEvent.save()

    

if __name__ == "__main__":
    """ This is executed when run from the command line """
    unittest.main()  