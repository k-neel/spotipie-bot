from sp_bot import SESSION
from bson import ObjectId


class MongoOperations:

    def __init__(self, SESSION):
        self.db = SESSION['spotipie']
        self.cursor1 = self.db['codes']
        self.cursor2 = self.db['users']

    def fetchCode(self, _id):
        query = {'_id': _id}
        return self.cursor1.find_one(query)

    def deleteCode(self, _id):
        query = {'_id': _id}
        self.cursor1.delete_one(query)

    def fetchData(self, tg_id):
        query = {'tg_id': tg_id}
        return self.cursor2.find_one(query)

    def updateData(self, tg_id, value):
        query = {'tg_id': tg_id}
        newvalues = {"$set": {"username": value}}
        self.cursor2.update_one(query, newvalues)

    def deleteData(self, tg_id):
        query = {'tg_id': tg_id}
        self.cursor2.delete_one(query)

    def countAll(self):
        return self.cursor2.find().count()

    def addUser(self, tg_id, token):
        User = {
            "username": "User",
            "token": token,
            "isAdmin": False,
            "tg_id": tg_id
        }
        user = self.cursor2.insert_one(User)
        return user


DATABASE = MongoOperations(SESSION)
