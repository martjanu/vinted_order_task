import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../application')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../application/rules')))

from datetime import datetime
from third_l_size_free import ThirdLSizeFree
from order import Order
from unittest.mock import MagicMock

class TestThirdLSizeFree(unittest.TestCase):

    def setUp(self):
        self.mock_provider = MagicMock()
        self.mock_provider.name = "LP"
        self.mock_provider.l_price = 10

        self.providers = [self.mock_provider]
        self.rule = ThirdLSizeFree(self.providers)

    def test_apply_discount_on_3rd_order(self):
        order1 = Order(date="2025-02-01", size="L", provider_name="LP")
        order1.price = 20
        order1.discount = 5

        order2 = Order(date="2025-02-15", size="L", provider_name="LP")
        order2.price = 25
        order2.discount = 8

        order3 = Order(date="2025-02-20", size="L", provider_name="LP")
        order3.price = 30
        order3.discount = 10

        updated_order1 = self.rule.apply_rule(order1)
        updated_order2 = self.rule.apply_rule(order2)
        updated_order3 = self.rule.apply_rule(order3)

        self.assertEqual(updated_order1.discount, 5)
        self.assertEqual(updated_order2.discount, 8)
        self.assertEqual(updated_order3.price, 0)
        self.assertEqual(updated_order3.discount, 10)

    def test_no_discount_on_non_L_size(self):
        order = Order(date="2025-02-01", size="M", provider_name="LP")
        order.price = 20
        order.discount = 5

        updated_order = self.rule.apply_rule(order)

        self.assertEqual(updated_order.discount, 5)
        self.assertEqual(updated_order.price, 20)

    def test_no_discount_on_non_LP_provider(self):
        order = Order(date="2025-02-01", size="L", provider_name="OtherProvider")
        order.price = 20
        order.discount = 5

        updated_order = self.rule.apply_rule(order)

        self.assertEqual(updated_order.discount, 5)
        self.assertEqual(updated_order.price, 20)

    def test_discount_not_applied_before_3rd_order(self):
        order1 = Order(date="2025-02-01", size="L", provider_name="LP")
        order1.price = 20
        order1.discount = 5

        order2 = Order(date="2025-02-10", size="L", provider_name="LP")
        order2.price = 25
        order2.discount = 8

        updated_order1 = self.rule.apply_rule(order1)
        updated_order2 = self.rule.apply_rule(order2)

        self.assertEqual(updated_order1.discount, 5)
        self.assertEqual(updated_order1.price, 20)

        self.assertEqual(updated_order2.discount, 8)
        self.assertEqual(updated_order2.price, 25)

    def test_no_discount_after_order_is_3rd_in_the_month(self):
        order1 = Order(date="2025-02-01", size="L", provider_name="LP")
        order1.price = 20
        order1.discount = 5

        order2 = Order(date="2025-02-15", size="L", provider_name="LP")
        order2.price = 25
        order2.discount = 8

        order3 = Order(date="2025-02-20", size="L", provider_name="LP")
        order3.price = 30
        order3.discount = 10

        updated_order1 = self.rule.apply_rule(order1)
        updated_order2 = self.rule.apply_rule(order2)
        updated_order3 = self.rule.apply_rule(order3)

        self.assertEqual(updated_order1.discount, 5)
        self.assertEqual(updated_order1.price, 20)

        self.assertEqual(updated_order2.discount, 8)
        self.assertEqual(updated_order2.price, 25)

        self.assertEqual(updated_order3.price, 0)
        self.assertEqual(updated_order3.discount, 10)

    def tearDown(self):
        del self.rule
        del self.providers

if __name__ == '__main__':
    unittest.main()
