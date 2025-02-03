import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../application')))

from rule import Rule

class CheapestSSize(Rule):
    def __init__(self, providers):
        self.providers = {provider.name: provider.s_price for provider in providers}

    def apply_rule(self, order):
        if order.size == 'S':
            cheapest_s_price = self.get_cheapest_s_price()
            current_s_price = self.get_current_s_price(order)
            order.price = cheapest_s_price
            order.discount += max(0, current_s_price - cheapest_s_price)

        return order

    def get_cheapest_s_price(self):
        return min(self.providers.values())

    def get_current_s_price(self, order):
        return self.providers.get(order.provider_name, float('inf'))
