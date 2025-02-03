from rule import Rule
from datetime import datetime

class MaxMonthlyDiscount(Rule):
    def __init__(self, monthly_discount_amount=10):
        self.monthly_discount_amount = monthly_discount_amount
        self.remaining_monthly_discounts = {}

    def apply_rule(self, order):
        month = order.date.strftime("%Y-%m")

        if month not in self.remaining_monthly_discounts:
            self.remaining_monthly_discounts[month] = self.monthly_discount_amount

        self._apply_discount(order, month)

        return order

    def _apply_discount(self, order, month):
        available_discount = self.remaining_monthly_discounts[month]

        if order.discount <= available_discount:
            self.remaining_monthly_discounts[month] -= order.discount
        else:
            excess_discount = order.discount - available_discount
            order.price += excess_discount
            order.discount = available_discount
            self.remaining_monthly_discounts[month] = 0
