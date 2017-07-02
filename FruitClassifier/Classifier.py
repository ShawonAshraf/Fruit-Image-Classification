import os
import tensorflow as tf

from matplotlib import pyplot as plt
from matplotlib import image as mat_img


class Classifier:
    def __init__(self, img_path):
        self.img_path = img_path
        self.image_name = os.path.split(self.img_path)[-1]
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


    def __str__(self):
        return 'Image Classifier : {}'.format(type(self))

    def classify_fruit(self):
        try:
            # read in image data
            image_data = tf.gfile.FastGFile(self.img_path, 'rb').read()

            # load labels
            label_lines = [line.rstrip() for line
                           in tf.gfile.FastGFile('../BasicClassifier/retrained_labels.txt')]

            # graph from file

            graph_file = tf.gfile.FastGFile('../BasicClassifier/retrained_graph.pb', 'rb')
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(graph_file.read())
            tf.import_graph_def(graph_def, name='')

            # create tf session

            sess = tf.Session()
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

            predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})

            # sorts the result in descending order
            top_predict = predictions[0].argsort()[-len(predictions[0]):][::-1]

            print('Result for {} :\n'.format(self.image_name))
            node_id = 1  # gets the best result since it's sorted

            label_string = label_lines[node_id]
            confidence_score = predictions[0][node_id]

            print('Label : {}\t Score : {}\n\n'.format(label_string, confidence_score))

        except Exception:
            print('Error! Image not found')


    # plots the image using matplotlib
    def plot_img(self):
        image = mat_img.imread(self.img_path)
        plt.axis('off')
        plt.imshow(image)
        plt.show()




# test

img_path = '../BasicClassifier/img_test/gvr.jpg'
cls = Classifier(img_path)
cls.classify_fruit()
# cls.plot_img()