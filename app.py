import os 
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)
import tensorflow as tf 
from tensorflow import keras
from keras.models import load_model 
from keras.backend import set_session
from skimage.transform import resize 
import matplotlib.pyplot as plt 
import numpy as np
from PIL import ImageOps, Image

print("Loading model") 
#global sess
#sess = tf.compat.v1.Session()
#set_session(sess)
global model 
model = load_model('durian_classification_trained_model.h5') 
#global graph
#graph = tf.compat.v1.get_default_graph()

@app.route('/', methods=['GET', 'POST']) 
def main_page():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads', filename))
        return redirect(url_for('prediction', filename=filename))
    return render_template('index.html')

@app.route('/prediction/<filename>') 
def prediction(filename):
    #Step 1
#     img = plt.imread(os.path.join('uploads', filename))
    img = Image.open(os.path.join('uploads', filename))
    img.save("")
    #Step 2
    my_image = ImageOps.fit(img, (128,128))
    my_image_re = tf.keras.applications.vgg16.preprocess_input(np.array(my_image))
#     f, axarr = plt.subplots(1,2)
#     axarr[0].imshow(my_image)
#     axarr[1].imshow(my_image_re)

    #Step 3
    #with graph.as_default():
        #set_session(sess)
        #Add
    model.run_eagerly=True  
    probabilities = model.predict(np.array([my_image_re,]), verbose=0)[0,:]
    print(probabilities)
    #Step 4
    number_to_class = ['D13','D24','D197']
    index = np.argsort(probabilities)
    predictions = {
        "class1":number_to_class[index[2]],
        "class2":number_to_class[index[1]],
        "class3":number_to_class[index[0]],
        "prob1":probabilities[index[2]],
        "prob2":probabilities[index[1]],
        "prob3":probabilities[index[0]],
        }
    #Step 5
    return render_template('predict.html', predictions=predictions)    

# @app.route('/prediction/<filename>') 
# def prediction(filename):
#     #Step 1
#     my_image = plt.imread(os.path.join('uploads', filename))
#     #Step 2
# #     my_image_re = resize(my_image, (32,32,3))
#     my_image_re = tf.keras.applications.vgg16.preprocess_input(my_image)
    
#     #Step 3
#     #with graph.as_default():
#       #set_session(sess)
#       #Add
#     model.run_eagerly=True  
#     probabilities = model.predict(np.array( [my_image_re,] ))[0,:]
#     print(probabilities)
#     #Step 4
#     number_to_class = ['D13', 'D24', 'D197']
#     index = np.argsort(probabilities)
#     predictions = {
#       "class1":number_to_class[index[9]],
#       "class2":number_to_class[index[8]],
#       "class3":number_to_class[index[7]],
#       "prob1":probabilities[index[9]],
#       "prob2":probabilities[index[8]],
#       "prob3":probabilities[index[7]],
#      }
#     #Step 5
#     return render_template('predict.html', predictions=predictions)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
