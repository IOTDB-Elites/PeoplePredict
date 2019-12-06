import random

import numpy as np
from sklearn import linear_model

from peoplePredict.model.util import data_to_correlation_feature as data_load


def max_index(matrix_prev, matrix_now, sample_rate=1):
    '''
    This method compares the people number in each position
    at time {t} and time {t-1}. For each position in time
    {t}, it randomly selects certain number of positions
    in {t-1}, calculate correlation and choose the one with
    maximum value, add it to the result list.
    :param matrix_prev: People number matrix of previous time.
           Each row is a number times eries on a position.
    :param matrix_now: People number matrix of present time.
           The columns number should be equal to matrix_prev's.
    :param sample_rate: for each position in matrix_now,
           it should compare to {matrix_prev.row_num * sample_rate}
           positions in matrix_prev, and select the one
           with maximum correlation value. The default value is 1.
    :return: a list. The i-th element k indicate that the i-th
             position in matrix_now is correlated
             with k-th position in matrix_pre. The number of elements
             should be equal to matrix_now.row_num
    '''
    r1, c1 = matrix_prev.shape
    r2, c2 = matrix_now.shape
    if c1 != c2:
        raise RuntimeError('columns number are different')
    index = []
    sample_num = int(r1 * sample_rate)
    for i in range(0, r2):
        # print(i)
        # time_start = time.time()
        select_index = list(range(0, r1))
        random.shuffle(select_index)
        select_index = select_index[0: sample_num]
        max_i = -1
        max_v = 0
        for j in select_index:
            cor = np.abs(np.corrcoef(matrix_now[i], matrix_prev[j])[0, 1])
            if cor > max_v:
                max_v = cor
                max_i = j
        if max_i == -1:
            max_i = 0
        index.append(max_i)
        # time_end = time.time()
        # print('totally cost', time_end - time_start)
    return np.array(index)


def train_linear_model(matrix_prev, matrix_now, index_list):
    '''
    This method trains the linear model
    :param matrix_prev: matrix_prev: People number matrix of previous time.
           Each row is a number times eries on a position.
    :param matrix_now: matrix_now: People number matrix of present time.
           The columns number should be equal to matrix_prev's.
    :param index_list: A list of index. The i-th element k indicate that
           the i-th position in matrix_now is correlated with k-th position
           in matrix_pre. The number of elements should be equal to
           matrix_now.row_num
    :return: a list of trained parameters. Each element is a pair of w and b,
             considering the model as y = w*x + b
    '''
    r1, c1 = matrix_prev.shape
    r2, c2 = matrix_now.shape
    linear = linear_model.LinearRegression()
    if c1 != c2:
        raise RuntimeError('columns number are different')
    p = []
    for i in range(0, r2):
        x = matrix_prev[index_list[i]].reshape((-1, 1))
        y = matrix_now[i]
        linear.fit(x, y)
        p.append([linear.coef_[0], linear.intercept_])
    return np.array(p)


if __name__ == '__main__':
    m, l = data_load.build_matrix()
    n = m.shape[0]
    model_max_index = []
    model_parameter = []
    for i in range(0, n - 1):
        index_list = max_index(m[i], m[i + 1], sample_rate=0.01)
        model_max_index.append(index_list)
        parameter_list = train_linear_model(m[i], m[i + 1], index_list)
        model_parameter.append(parameter_list)
    model_max_index = np.array(model_max_index)
    model_parameter = np.array(model_parameter)
    np.save("../data/model_max_index", model_max_index)
    np.save("../data/model_parameter", model_parameter)