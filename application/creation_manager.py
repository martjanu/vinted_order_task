import  os
import  sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './providers')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './rules')))

from lp import LP
from mr import MR

from cheapest_s_size import CheapestSSize
from max_monthly_discount import MaxMonthlyDiscount
from third_l_size_free import ThirdLSizeFree

from order import Order


class CreationManager:
    def create_providers(self):
        return [
            LP(),
            MR()
        ]

    def create_order(self, line):
        date = line.split()[0]
        size = line.split()[1]
        provider_name = line.split()[2]

        return Order(date, size, provider_name)

    def create_rules(self):
        return [
            CheapestSSize(self.create_providers()),
            ThirdLSizeFree(self.create_providers()),
            MaxMonthlyDiscount()
        ]