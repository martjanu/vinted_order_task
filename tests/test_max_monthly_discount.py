import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../application')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../application/rules')))

from datetime import datetime
from max_monthly_discount import MaxMonthlyDiscount
from order import Order

class TestMaxMonthlyDiscount(unittest.TestCase):

    def setUp(self):
        self.rule = MaxMonthlyDiscount(monthly_discount_amount=10)

    def test_apply_discount_within_limit(self):
        order = Order(date="2025-02-01", size="S", provider_name="Provider1")
        order.price = 20
        order.discount = 5
        updated_order = self.rule.apply_rule(order)
        self.assertEqual(updated_order.discount, 5)
        self.assertEqual(updated_order.price, 20)

    def test_apply_discount_exceeding_limit(self):
        order = Order(date="2025-02-01", size="S", provider_name="Provider1")
        order.price = 20
        order.discount = 15
        updated_order = self.rule.apply_rule(order)
        self.assertEqual(updated_order.discount, 10)
        self.assertEqual(updated_order.price, 25)

    def test_apply_multiple_orders_same_month(self):
        order1 = Order(date="2025-02-01", size="S", provider_name="Provider1")
        order1.price = 20
        order1.discount = 6
        updated_order1 = self.rule.apply_rule(order1)

        order2 = Order(date="2025-02-15", size="S", provider_name="Provider2")
        order2.price = 30
        order2.discount = 8
        updated_order2 = self.rule.apply_rule(order2)

        self.assertEqual(updated_order1.discount, 6)
        self.assertEqual(updated_order1.price, 20)

        self.assertEqual(updated_order2.discount, 4)
        self.assertEqual(updated_order2.price, 34)

    def test_apply_discount_next_month(self):
        order = Order(date="2025-03-01", size="S", provider_name="Provider1")
        order.price = 20
        order.discount = 15
        updated_order = self.rule.apply_rule(order)
        self.assertEqual(updated_order.discount, 10)
        self.assertEqual(updated_order.price, 25)

    def tearDown(self):
        del self.rule

if __name__ == '__main__':
    unittest.main()
