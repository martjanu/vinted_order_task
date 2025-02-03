from datetime import datetime

class Order:
    def __init__(self, date, size, provider_name):
        self.date = datetime.strptime(date, "%Y-%m-%d").date()
        self.size = size
        self.provider_name = provider_name
        self.price = None
        self.discount = 0

    def __str__(self):
        return f"{self.date} {self.size} {self.provider_name} {self.price} {self.discount }"