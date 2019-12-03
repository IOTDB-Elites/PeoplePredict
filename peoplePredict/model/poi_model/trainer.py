from peoplePredict.model.poi_model.nn import NN
from peoplePredict.model.util.data_to_poi_feature import build_data_poi_feature, generate_batch
import tensorflow as tf
import os
import numpy as np

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
            ckpt = tf.train.get_checkpoint_state('../data/poi_model/nn_model')
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
                          sess.run([model.loss], feed_dict={model.x: x, model.y: y, model.keep_prob: 0.7}))
                    print("step:", "valid:",
                          sess.run([model.loss], feed_dict={model.x: valid_x, model.y: valid_y, model.keep_prob: 1}))
                    # valid_accuracy = sess.run(accuracy, feed_dict={xs: valid_x, ys: valid_y})
                    # print("step %d, training accuracy %g" % (i, train_accuracy))
                    # print("step %d, valid accuracy %g" % (i, valid_accuracy))
                    #
                    # y_label_result, y_true_result = sess.run([y_label, y_true], feed_dict={xs: valid_x, ys: valid_y})
                    # print("f1_score", sk.metrics.f1_score(y_label_result, y_true_result, average = "weighted"))
                    # exit(0)
                    # print(y_label)
                    # print(_index)

                    saver.save(sess, "./xkf_nn_model/nn", global_step=i)

                _, summary = sess.run([model.train_op, merged], feed_dict={model.x: x, model.y: y, model.keep_prob: 1})
                writer.add_summary(summary, i)
                _, summary = sess.run([model.train_op, merged],
                                      feed_dict={model.x: x_valid, model.y: y_valid, model.keep_prob: 1})
                writer.add_summary(summary, i)
                # _, summary = sess.run([model.train_op, merged], feed_dict={model.x: x_test, model.y: y_test, model.keep_prob: 1})
                # writer.add_summary(summary, i)