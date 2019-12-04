import datetime

from peoplePredict.database.dao import Dao
import random
import numpy as np


def day_to_weekday(year, month, day):
    d = datetime.date(year, month, day)
    return d.weekday()


def build_data_poi_feature():
    dao = Dao()
    x = []
    y = []

    count = 0
    for row in dao.read_data():
        cur_x = [day_to_weekday(row['year'], row['month'], row['day']), row['hour'],
                 row['lng_gcj02'], row['lat_gcj02'], int(row['typecode'])]

        x.append(cur_x)
        y.append(row['value'])

        count += 1
        if count % 10000 == 0:
            print(count)

    dao.close()

    np.savez('../data/poi_model/feature', x=x, y=y)
    return np.array(x), np.array(y)


def generate_batch(batch_size, data_x, data_y):
    x = np.ndarray([batch_size, len(data_x[0])], dtype=float)
    y = np.ndarray([batch_size, 1], dtype=int)

    for i in range(batch_size):
        index = random.randint(0, len(data_x) - 1)
        x[i] = data_x[index]
        y[i] = data_y[index]

    return x, y


def build_predict_data():
    dao = Dao()
    predict_row = set()

    count = 0
    for row in dao.read_data():
        cur_x = (row['lng_gcj02'], row['lat_gcj02'], int(row['typecode']))
        predict_row.add(cur_x)

        count += 1
        if count % 10000 == 0:
            print(count)

    x = []
    for point in predict_row:
        for day in (1, 2, 3, 4, 5, 6, 0):
            for hour in [7, 12, 15, 20, 21]:
                x.append([day, hour, point[0], point[1], point[2]])

    x = np.array(x)
    # x -> [[day, hour, lng_gcj02, lat_gcj02, typecode],...]
    np.savez('../data/poi_model/predict', x=x)

    return x


if __name__ == '__main__':
    x = build_predict_data()
    print(x.shape)
