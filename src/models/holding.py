#
# Author: Robert Patel
# Holding class which contains getters/setters for Holding object.
#

class Holding:

    # Constructs a new Holding object.
    def __init__(self, ticker: str, quantity: int, price_per_share: float, purchase_price: float):
        self.ticker = ticker
        self.quantity = quantity
        self.price_per_share = price_per_share
        self.purchase_price = purchase_price

    # Gets the ticker
    def get_ticker(self) -> str:
        return self.ticker
    
    # Sets the ticker
    def set_ticker(self, ticker: str):
        self.ticker = ticker

    # Gets the quantity of the holding.
    def get_quantity(self) -> int:
        return self.quantity
    
    # Sets the quantity of the holding.
    def set_quantity(self, quantity: int):
        self.quantity = quantity
    
    # Gets the price_per_share of the holding.
    def get_price_per_share(self) -> float:
        return self.price_per_share
    
    # Sets the price_per_share of the holding.
    def set_price_per_share(self, price_per_share: float):
        self.price_per_share = price_per_share

    # Gets the purchase_price of the holding.
    def get_purchase_price(self) -> float:
        return self.purchase_price
    
    # Gets the current_value of the holding.
    def get_current_value(self) -> float:
        return self.quantity * self.price_per_share
    
    # Calculate gain/loss of the holding.
    def calculate_gain_or_loss(self) -> float:
        return (self.price_per_share - self.purchase_price) * self.quantity

