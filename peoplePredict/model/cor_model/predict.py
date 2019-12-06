import numpy as np

def get_first():

    return []

def predict(prev, index_list, parameter_list):
    return int(prev[index_list] * parameter_list[0] + parameter_list[1])

if __name__ == '__main__':
    for i in range(0, 7):
        data1 = get_first()
        model_index = np.load("../data/model_max_index")
        model_parameter = np.load("../data/model_parameter")
        data2 = predict(data1, model_index[0], model_parameter[0])
        data3 = predict(data2, model_index[1], model_parameter[1])
        data4 = predict(data3, model_index[2], model_parameter[2])
        data5 = predict(data4, model_index[3], model_parameter[3])
