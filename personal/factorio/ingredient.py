
class ProductInput:
    def __init__(self, product, q, lanes=None):
        self.product = product
        # qantity
        self.q = q
        # number of dedicated lanes for input
        self.lanes = lanes

    def mul(self, x):
        return ProductInput(self.product, self.q * x)




