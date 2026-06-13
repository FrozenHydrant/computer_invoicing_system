from decimal import *

class Item:

    # SubItem class for little mini items that go inside
    class SubItem:
        def __init__(self, title: str):
            self.title = title
            self.has_price = False
            self.has_cost = False


        def set_price(self, new_price: Decimal):
            self.has_price = True
            self.price = new_price


        def set_cost(self, new_cost: Decimal):
            self.has_cost = True
            self.cost = new_cost

    
    def __init__(self, title: str, price: Decimal, cost: Decimal):
        self.title = title
        self.price = price 
        self.cost = cost

        self.subitems: dict[str, SubItem] = {}
    
    
    def add_subitem(self, key: str, subitem: SubItem):
        self.subitems[key] = subitem