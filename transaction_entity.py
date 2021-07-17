# Transaction object for each transaction
class TransactionEntity:

    def __init__(self, payer=None, points=None, timestamp=None):
        self.payer = payer
        self.points = points
        self.timestamp = timestamp
