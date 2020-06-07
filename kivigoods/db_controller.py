from pymongo import MongoClient

class DbController():
    def __init__(self):
        client = MongoClient()
        db = client['kivy_goods_db']
        collection = db['kivy_goods-collection']

        self.goodsList = collection

    def addItem(self, item, quantity):
        db_item = self.goodsList.find_one({ 'item': item })
        if not db_item:
            self.goodsList.insert_one( { 'item': item, 'quantity': quantity } ).inserted_id

        else:
            quantity_ = float(quantity) + float(db_item['quantity'])
            self.goodsList.update_one({
                '_id': db_item['_id']
            },{
                '$set': {
                    'quantity': quantity_
                }
            }, upsert=False)

        return self.goodsList.find_one({ 'item': item })

    def getList(self):
        return [{'item': good['item'], 'quantity': good['quantity']} for good in self.goodsList.find()]

    def deleteItem(self, item):
        self.goodsList.remove( { 'item' : item } );