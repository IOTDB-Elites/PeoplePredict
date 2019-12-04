from peoplePredict.model.poi_model.nn import NN
from peoplePredict.model.util.data_to_poi_feature import build_data_poi_feature, generate_batch
import tensorflow as tf
import os
import numpy as np

MODEL_LOC = '../data/poi_model/nn_model/nn'
training_batch_size = 256
valid_batch_size = 256
iteration = 100000
##


if __name__ == '__main__':
    print("reading data from training set...")

    if os.path.exists("../data/poi_model/feature" + ".npz"):
        zip_file = np.load("../data/poi_model/feature" + ".npz")
        train_x = zip_file['x']
        train_y = zip_file['y']
    else:
        print("No dump file! Reading from original file! Please wait... ")
        train_x, train_y = build_data_poi_feature()

    print("reading complete!")
    model = NN()

    x, y = generate_batch(model.training_batch_size, train_x, train_y)
    print(train_x.shape)

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

            # 可视化部分
            tf.summary.scalar("loss", model.loss)
            merged = tf.summary.merge_all()
            writer = tf.summary.FileWriter('../data/poi_model/nn_logs', sess.graph)

            # training part
            for i in range(iteration):
                x, y = generate_batch(model.training_batch_size, train_x, train_y)
                x_valid, y_valid = generate_batch(model.valid_batch_size, train_x, train_y)

                if i % 1000 == 0:
                    # train_accuracy = sess.run(accuracy, feed_dict={xs: x, ys: y})
                    valid_x, valid_y = generate_batch(model.valid_batch_size, train_x, train_y)
                    print("step:", i, "train:",
                          sess.run([model.mean_square], feed_dict={model.x: x, model.y: y, model.keep_prob: 1}))
                    print("step:", "valid:",
                          sess.run([model.mean_square], feed_dict={model.x: valid_x, model.y: valid_y, model.keep_prob: 1}))

                    saver.save(sess, MODEL_LOC, global_step=i)

                _, summary = sess.run([model.train_op, merged], feed_dict={model.x: x, model.y: y, model.keep_prob: 0.7})
                writer.add_summary(summary, i)
