from pymongo import MongoClient
from peoplePredict.database.constant import port, uri, join_database


class Dao:
    def __init__(self):
        self.conn = MongoClient(uri, port=port)
        self.db = self.conn.qh_area_forecast
        self.people_num_join_poi = self.db[join_database]

    # use cursor to read
    def read_data(self):
        return self.people_num_join_poi.find()

    def close(self):
        self.conn.close()


# just a example for reading data
if __name__ == '__main__':
    dao = Dao()
    count = 0
    for i in dao.read_data():
        count += 1
        if count % 1000 == 0:
            print(count)
            print(i)
    # do not forget this
    dao.close()

    print("total len: ", count)
