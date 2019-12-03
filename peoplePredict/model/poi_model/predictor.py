from peoplePredict.database.dao import Dao
from peoplePredict.model.poi_model.nn import NN
from peoplePredict.model.util.data_to_poi_feature import build_predict_data
import tensorflow as tf
import os
import numpy as np

##

DATABASE = 'poi_model_result'

if __name__ == '__main__':
    print("reading data from training set...")

    if os.path.exists("../data/poi_model/predict" + ".npz"):
        zip_file = np.load("../data/poi_model/predict" + ".npz")
        x = zip_file['x']
    else:
        print("No dump file! Reading from original file! Please wait... ")
        x = build_predict_data()

    print(x.shape)
    exit(-1)
    print("reading complete!")
    model = NN()

    print("data load complete")
    print("The model begin here")

    # run part
    with model.graph.as_default():
        with tf.Session() as sess:
            # 初始化变量
            sess.run(tf.global_variables_initializer())
            # 保存参数所用的保存器
            saver = tf.train.Saver(max_to_keep=1)
            # get latest file
            ckpt = tf.train.get_checkpoint_state('../data/poi_model/nn_model')
            if ckpt and ckpt.model_checkpoint_path:
                saver.restore(sess, ckpt.model_checkpoint_path)
            else:
                print("no model, exit!")
                exit(-1)

            dao = Dao()
            cache = []
            count = 0
            for row_x in x:
                # val = 0
                print(sess.run([model.result], feed_dict={model.x: x.reshape(1, x.shape[0]), model.keep_prob: 1}))
                # cache.append({'month' : 10,
                #               'day' : row_x[0],
                #               'hour': row_x[1],
                #               'lng_gcj02' : row_x[2],
                #               'lat_gcj02' : row_x[3],
                #               'value': val})
                #
                # if len(cache) == 100:
                #     count += 100
                #     dao.insert_many(DATABASE, cache)
                #     cache.clear()
                #     if count % 1000 == 0:
                #         print(count)

            dao.close()





