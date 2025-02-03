from provider import  Provider

class MR(Provider):
    def __init__(self):
        self.name = 'MR'
        self.sizes = ['S', 'M', 'L']
        self.s_price = 2
        self.m_price = 3
        self.l_price = 4