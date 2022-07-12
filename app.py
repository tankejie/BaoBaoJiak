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
# filename = ""


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
#     img.save("https://github.com/tankejie/BaoBaoJiak/blob/main/uploads/uploadimage.jpg")
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
    # converting probabilities to percentages
    percentages = [round(p*100,2) for p in probabilities]
    #Step 4
    number_to_class = ['Singapore Red Prawn (D13)','Sultan (D24)','Mao Shan Wang (D197)']
    index = np.argsort(percentages)
    if number_to_class[index[2]] == "Mao Shan Wang (D197)":
        description = "Mao Shan Wang AKA: Butter durian, Cat Mountain King, Rajah Kunyit. Probably the most popular type of durian among Singaporeans besides the D24. Rich in taste and color, Mao Shan Wang durians boast a creamy texture and leave a strong bittersweet taste in your mouth. To distinguish them, look out for the pyramid-shapes thorns at the base of the stem. They also have a unique starfish-shaped pattern found at the base of the durian fruit."
#         description = "MSW"
    elif number_to_class[index[2]] == "Sultan (D24)":
        description = "Before the Mao Shan Wang breed surged in popularity, the most famous breed back in the ’90s was the D24 durians. D24 durians are a little less overwhelming in flavour and are known for their creamy texture and subtle bittersweet after-taste. If you’re not that familiar with durians, this is a good introduction to the king of fruits. The stem of the durian is shorter compared to other durians and it has a brown-coloured ring around the bottom of the stem."
#         description = "D24"
    elif number_to_class[index[2]] == "Singapore Red Prawn (D13)":
        description = "Originating from Johor, D13 durians are also known as the 'kampung' breed with a sticky texture. It is perhaps one of the many highly-sought-after durian species with a bright orange flesh and large seeds which makes it easier to enjoy."
#         description = "D13"
    else:
        description = "To be added"
    predictions = {
        "class1":number_to_class[index[2]],
        "class2":number_to_class[index[1]],
        "class3":number_to_class[index[0]],
        "prob1":percentages[index[2]],
        "prob2":percentages[index[1]],
        "prob3":percentages[index[0]],
        "description":description
    }
    #Step 5
    return render_template('predict.html', predictions=predictions)

@app.route('/prediction/' + filename, methods=['GET', 'POST'])
def prediction_page():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads', filename))
        return redirect(url_for('prediction', filename=filename))
    return render_template('index.html')

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
