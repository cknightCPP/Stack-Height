import StackHeight as sh
import unittest
class add_test(unittest.TestCase):
    def test(self):
        self.assertEquals(3,sh.add(1,2))
