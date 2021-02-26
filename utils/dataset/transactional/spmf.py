from utils.dataset.database import Database


class VerticalView:
    items = dict()

    def __init__(self):
        pass

    def add_transaction(self, transaction, transaction_id):
        for item in transaction:
            if item not in self.items.keys():
                self.items[item] = list()
            self.items[item].append(transaction_id)

    def pop(self, key):
        return self.items.pop(key)

    def include_transactions(self, transactions):
        items = list()
        for item in self.items.keys():
            if transactions in self.items[items]:
                items.append(item)
        return items


class HorizontalView:
    transactions = dict()

    def __init__(self):
        pass

    def add_transaction(self, transaction):
        self.transactions[self.transactions.__len__()] = transaction

    def pop(self, key):
        return self.transactions.pop(key)

    def include_item_set(self, item_set):
        transaction_ids = list()
        for transaction_id, transaction in enumerate(self.transactions.keys()):
            if item_set in self.transactions[transaction]:
                transaction_ids.append(transaction_id)
        return transaction_ids


class Dataset(Database):

    def __init__(self, file):
        super().__init__(file)

    def transactions(self):
        self.data_set.seek(0)
        while (transaction := self.data_set.readline().strip().split(' ')) != ['']:
            yield transaction


class Datasets:
    accidents = 'data/accidents.spmf'
    bible = 'data/bible.spmf'
    chainsotreFIM = 'data/chainsotreFIM.spmf'
    chess = 'data/chess.spmf'
    connect = 'data/connect.spmf'
    foodmartFIM = 'data/foodmartFIM.spmf'
    kddcup99 = 'data/kddcup99.spmf'
    kosarak = 'data/kosarak.spmf'
    mushrooms = 'data/mushrooms.spmf'
    MSNBC = 'data/MSNBC.spmf'
    pumsb = 'data/pumsb.spmf'
    retail = 'data/retail.spmf'
