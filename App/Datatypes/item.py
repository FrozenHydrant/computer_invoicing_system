from decimal import *

class Item:

    def __init__(self, title: str, price: Decimal, cost: Decimal):
        self.title = title
        self.price = price 
        self.cost = cost

        self.subitems = {}