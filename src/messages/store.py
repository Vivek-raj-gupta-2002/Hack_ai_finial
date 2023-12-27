from uagents import Model


class Search(Model):
    item_name: str
    max_price: float = None
    min_price: float =None
    

class PlaceOrder(Model):
    item: dict