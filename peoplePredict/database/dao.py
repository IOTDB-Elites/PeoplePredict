from pymongo import MongoClient
from peoplePredict.database.constant import port, uri, join_database, poi_database, people_num_database


class Dao:
    def __init__(self):
        self.conn = MongoClient(uri, port=port)
        self.db = self.conn.qh_area_forecast
        self.people_num_join_poi = self.db[join_database]

    # use cursor to read
    def read_data(self, filter=None):
        if not filter:
            return self.people_num_join_poi.find()

        return self.people_num_join_poi.find(filter)

    # insert into db_name, example is here
    # ```
    # DATABASE = 'your_name'
    # dao = Dao()
    # cache = []
    # count = 0
    #
    # dao.clear_database(DATABASE)
    # for row in your_data:
    #     cache.append({'month': 10,
    #                   'day': row[0],
    #                   'hour': row[1],
    #                   'lng_gcj02': row[2],
    #                   'lat_gcj02': row[3],
    #                   'value': row[4])})
    #
    #     if len(cache) == 100:
    #         count += 100
    #         dao.insert_many(DATABASE, cache)
    #         cache.clear()
    #         if count % 1000 == 0:
    #             print(count)
    # if len(cache) != 0:
    #     dao.insert_many(DATABASE, cache)
    # dao.close()
    # ```
    def insert_many(self, db_name, data_list):
        self.db[db_name].insert_many(data_list)

    # clear database
    def clear_database(self, db_name, filter=None):
        # security check
        if db_name == join_database or db_name == poi_database or db_name == people_num_database:
            print("Delete raw database is forbidden")
            exit(-1)

        return self.db[db_name].delete_many({} if filter is None else filter)

    # read data from db_name
    def read_data_from_target_database(self, db_name, filter=None):
        if not filter:
            return self.db[db_name].find()
        return self.db[db_name].find(filter)

    def close(self):
        self.conn.close()


# just a example for reading data
if __name__ == '__main__':
    dao = Dao()
    count = 0
    for i in dao.read_data_from_target_database('integrated_result', {'month': 9, 'day': {'$gt': 23}}):
        count += 1
        if count % 10000 == 0:
            print(i)

    # do not forget this
    print(count)
    dao.close()

    print("total len: ", count)
