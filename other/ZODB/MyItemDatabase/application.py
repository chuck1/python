import ZODB, ZODB.FileStorage
import BTrees
import transaction
import persistent

class NumberGenerator(persistent.Persistent):
    def __init__(self):
        self.number = 0

    def next(self):
        i = self.number
        self.number += 1
        return "TEMP{}".format(i)

class ItemManager(persistent.Persistent):
    def __init__(self):
        self.tree = BTrees.OOBTree.BTree()
        self.numberGenerator = NumberGenerator()

    def add(self, item):
        
        for k,v in self.tree.items():
            if v == item:
                print "equivalent item already in database"
                return

        
        if item.itemNumber is None:
            item.itemNumber = self.numberGenerator.next()
        
        self.tree[item.itemNumber] = item

class Application(object):

    def __init__(self):

        storage = ZODB.FileStorage.FileStorage('mydata.fs')
        db = ZODB.DB(storage)
        connection = db.open()
        self.root = connection.root

        try:
            print self.root.itemManager
        except:
            self.root.itemManager = ItemManager()


    def commit(self):
        transaction.commit()




