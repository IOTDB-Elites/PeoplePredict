from peoplePredict.database.dao import Dao
from peoplePredict.model.poi_model.nn import NN
from peoplePredict.model.util.data_to_poi_feature import build_predict_data
import tensorflow as tf
import os
import numpy as np

##

MODEL_LOC = '../data/poi_model/nn_model'
DATABASE = 'poi_model_result'
weekday_map = {1: 24, 2: 25, 3: 26, 4: 27, 5: 28, 6: 29, 0: 30}

if __name__ == '__main__':
    print("reading data from training set...")

    if os.path.exists("../data/poi_model/predict" + ".npz"):
        zip_file = np.load("../data/poi_model/predict" + ".npz")
        x = zip_file['x']
    else:
        print("No dump file! Reading from original file! Please wait... ")
        x = build_predict_data()


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
            ckpt = tf.train.get_checkpoint_state(MODEL_LOC)
            if ckpt and ckpt.model_checkpoint_path:
                saver.restore(sess, ckpt.model_checkpoint_path)
            else:
                print("no model, exit!")
                exit(-1)

            dao = Dao()
            cache = []
            count = 0

            dao.clear_database(DATABASE)
            for row_x in x:
                # val = 0
                val = sess.run \
                    ([model.result], feed_dict={model.x: row_x.reshape(1, row_x.shape[0]), model.keep_prob: 1})[0][0]
                cache.append({'year': 2019,
                              'month': 9,
                              'day': weekday_map[row_x[0]],
                              'hour': row_x[1],
                              'lng_gcj02': round(row_x[2], 3),
                              'lat_gcj02': round(row_x[3], 3),
                              'value': int(val)})

                if len(cache) == 100:
                    count += 100
                    dao.insert_many(DATABASE, cache)
                    cache.clear()
                    if count % 1000 == 0:
                        print(count)

            dao.close()
