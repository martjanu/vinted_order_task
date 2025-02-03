import datetime
import unittest
import  os
import  sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../application')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../application/providers')))

from creation_manager import CreationManager
from lp import LP
from mr import MR
from cheapest_s_size import CheapestSSize
from max_monthly_discount import MaxMonthlyDiscount
from third_l_size_free import ThirdLSizeFree
from order import Order


class TestCreationManager(unittest.TestCase):
    def setUp(self):
        self.creation_manager = CreationManager()

    def test_create_providers(self):
        providers = self.creation_manager.create_providers()
        self.assertEqual(len(providers), 2)
        self.assertIsInstance(providers[0], LP)
        self.assertIsInstance(providers[1], MR)

    def test_create_order(self):
        line = "2015-02-01 S MR"
        order = self.creation_manager.create_order(line)

        self.assertEqual(order.date, datetime.date(2015, 2, 1))
        self.assertEqual(order.size, "S")
        self.assertEqual(order.provider_name, "MR")

    def test_create_rules(self):
        rules = self.creation_manager.create_rules()
        self.assertEqual(len(rules), 3)
        self.assertIsInstance(rules[0], CheapestSSize)
        self.assertIsInstance(rules[1], ThirdLSizeFree)
        self.assertIsInstance(rules[2], MaxMonthlyDiscount)

    def tearDown(self):
        del self.creation_manager


if __name__ == '__main__':
    unittest.main()
