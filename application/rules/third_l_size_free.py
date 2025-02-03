from rule import Rule
from datetime import datetime

class ThirdLSizeFree(Rule):
    def __init__(self, providers):
        self.providers = {provider.name: provider.l_price for provider in providers}
        self.monthly_orders = {}

    def apply_rule(self, order):
        if self.is_eligible_for_discount(order):
            month = self.get_order_month(order)
            self.track_monthly_order(month)

            if self.monthly_orders[month] == 3:
                self.apply_discount(order, month)

        return order

    def is_eligible_for_discount(self, order):
        return order.size == 'L' and order.provider_name == 'LP'

    def get_order_month(self, order):
        return order.date.strftime("%Y-%m")

    def track_monthly_order(self, month):
        if month not in self.monthly_orders:
            self.monthly_orders[month] = 1
        elif self.monthly_orders[month] != -1:
            self.monthly_orders[month] += 1

    def apply_discount(self, order, month):
        self.monthly_orders[month] = -1
        order.price = 0
        order.discount = self.providers.get(order.provider_name, 0)
