#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 00:24:18 2025

@author: zacharywen
"""

# categories
X = 'kiwi'
Y = 'green beans'

# two example images for website
sampleX = 'static/kiwi.jpg'
sampleY = 'static/green_beans.jpg'

# location for user uploads
UPLOAD_FOLDER = 'static/uploads'
# allowed files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# load os library
import os

# load website libraries
from flask import render_template
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

# load math library
import numpy as np

# load ml libraries
from tensorflow.keras.preprocessing import image
from keras.models import load_model
from keras.backend import set_session
import tensorflow as tf


# create website object
app = Flask(__name__)


def load_model_from_file():
    mySession = tf.Session()
    set_session(mySession)
    myModel = load_model('saved_model.h5')
    myGraph = tf.get_default_graph()
    return (mySession,myModel,myGraph)

# make sure user uploaded file is a valid file
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# define view from top level page
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    # iniit webpage load
    if request.method == 'GET' :
        return render_template('index.html', myX=X, myY=Y, mySampleX=sampleX, mySampleY=sampleY)
    else:
        # check if post request has file
        if 'file' not in request.files:
            flash('No file part')
            return redirect(requeset.url)
        file = request.files['file']
        # if user does not select file, browser may also submit empty part w/o filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # if file extension isn't allowed
        if not allowed_file(file.filename):
            flash('Only the following extensions allowed: .png, .jpg, jpeg, .gif')
            return redirect(request.url)
        # file upload is successful
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
        
        
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    test_image = image.load_img(UPLOAD_FOLDER+"/"+filename,target_size=(150,150))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    
    mySession = app.config['SESSION']
    myModel = app.config['MODEL']
    myGraph = app.config['GRAPH']
    with myGraph.as_default():
        set_session(mySession)
        result = myModel.predict(test_image)
        image_src = "/"+UPLOAD_FOLDER+"/"+filename
        if result[0] < 0.5 :
            answer = "<div class='col text-center'><img width='150' height='150' src='"+image_src+"' class='img-thumbnail' /><h4>guess:"+X+" "+str(result[0])+"</h4></div><div class='col'></div><div class='w-100'></div>"
        else:
            answer = "<div class='col'></div><div class='col text-center'><img width='150' height='150' src='"+image_src+"' class='img-thumbnail' /><h4>guess:"+Y+" "+str(result[0])+"</h4></div><div class='w-100'></div>"
        results.append(answer)
        return render_template('index.html', myX=X, myY=Y, mySampleX=sampleX, mySampleY=sampleY)



def main():
    (mySession,myModel,myGraph) = load_model_from_file()
    
    app.config['SECRET_KEY'] = 'super secret key'
    
    app.config['SESSION'] = mySession
    app.config['MODEL'] = myModel
    app.config['GRAPH'] = myGraph
    
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #16MB upload limit
    app.run()
    
# create running list of results
results = []

# launch everything
main()