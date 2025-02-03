import unittest
import  os
import  sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../application/rules')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../application')))

from unittest.mock import MagicMock
from cheapest_s_size import CheapestSSize
from order import Order

class TestCheapestSSize(unittest.TestCase):

    def setUp(self):
        self.mock_provider1 = MagicMock()
        self.mock_provider1.name = "Provider1"
        self.mock_provider1.s_price = 10

        self.mock_provider2 = MagicMock()
        self.mock_provider2.name = "Provider2"
        self.mock_provider2.s_price = 15

        self.providers = [self.mock_provider1, self.mock_provider2]

        self.rule = CheapestSSize(self.providers)

    def test_apply_rule_with_size_s(self):
        order = Order(date="2025-02-01", size="S", provider_name="Provider1")
        updated_order = self.rule.apply_rule(order)
        self.assertEqual(updated_order.price, 10)
        self.assertEqual(updated_order.discount, 0)

    def test_apply_rule_with_non_s_size(self):
        order = Order(date="2025-02-01", size="M", provider_name="Provider1")
        order.price = 20
        order.discount = 0
        updated_order = self.rule.apply_rule(order)
        self.assertEqual(updated_order.price, 20)
        self.assertEqual(updated_order.discount, 0)

    def test_get_cheapest_s_price(self):
        cheapest_price = self.rule.get_cheapest_s_price()
        self.assertEqual(cheapest_price, 10)

    def test_get_current_s_price(self):
        order = Order(date="2025-02-01", size="S", provider_name="Provider1")
        current_price = self.rule.get_current_s_price(order)
        self.assertEqual(current_price, 10)
        order.provider_name = "Provider2"
        current_price = self.rule.get_current_s_price(order)
        self.assertEqual(current_price, 15)

    def tearDown(self):
        del self.rule
        del self.providers


if __name__ == '__main__':
    unittest.main()
