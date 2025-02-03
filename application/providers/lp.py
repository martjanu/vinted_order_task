from provider import  Provider

class LP(Provider):
    def __init__(self):
        self.name = 'LP'
        self.sizes = ['S', 'M', 'L']
        self.s_price = 1.5
        self.m_price = 4.5
        self.l_price = 6.9