import statsmodels.api as sm
import pandas as pd
import os
import numpy as np
from peoplePredict.model.util.data_to_arima_feature import build_matrix
from peoplePredict.database.dao import Dao
import time

hour_map = {0: 7, 1: 12, 2: 15, 3: 20, 4: 21}

forecast_step = 5*7

insert_frequency = forecast_step * 10

DATABASE = 'arima_model_result'


def arima_predict(data, p, d, q):
    dta = pd.Series(data)
    dta.index = pd.Index(sm.tsa.datetools.dates_from_range('2001', '2175'))
    ARIMA_model = sm.tsa.ARIMA(dta, order=(p, d, q)).fit(disp=-1)
    return ARIMA_model.forecast(steps=forecast_step)


if __name__ == '__main__':
    print("reading data from training set...")

    if os.path.exists("../data/arima_model/matrix" + ".npz"):
        zip_file = np.load("../data/arima_model/matrix" + ".npz")
        matrix = zip_file['matrix']
        location = zip_file['location']
    else:
        print("No dump file! Reading from original file! Please wait... ")
        matrix, location = build_matrix()

    print("reading complete!")

    res = []

    dao = Dao()
    dao.clear_database(DATABASE)
    count = 0
    start_time = time.time()
    for i in range(matrix.shape[0]):
        lng_gcj02 = round(float(location[i].split(",")[0]), 3)
        lat_gcj02 = round(float(location[i].split(",")[1]), 3)
        try:
            predict_data = arima_predict(matrix[i], 2, 1, 5)[0]
            for j in range(forecast_step):
                res.append({'year': 2019,
                            'month': 9,
                            'day': 24 + j // 5,
                            'hour': hour_map[j % 5],
                            'lng_gcj02': lng_gcj02,
                            'lat_gcj02': lat_gcj02,
                            'value': int(predict_data[j])})
        except ValueError:
            for j in range(forecast_step):
                res.append({'year': 2019,
                            'month': 9,
                            'day': 24 + j // 5,
                            'hour': hour_map[j % 5],
                            'lng_gcj02': lng_gcj02,
                            'lat_gcj02': lat_gcj02,
                            'value': int(matrix[i][j-forecast_step])})

        if len(res) == insert_frequency:
            count += 100
            dao.insert_many(DATABASE, res)
            res.clear()
            if count % 1000 == 0:
                print("count: ", count)

    dao.close()
