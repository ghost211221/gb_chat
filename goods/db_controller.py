from pymongo import MongoClient

class DbController():
    def __init__(self):
        client = MongoClient()
        db = client['goods_db']
        collection = db['goods-collection']

        self.goodsList = collection

    def addItem(self, item):
        id = self.goodsList.insert_one( { 'item': item } ).inserted_id

    def getList(self):
        return [good['item'] for good in self.goodsList.find()]

    def deleteItem(self, item):
        self.goodsList.remove( { 'item' : item } );