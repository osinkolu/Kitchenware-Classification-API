# -*- coding: utf-8 -*-
"""
Created on Tuesday January 30 19:35:03 2023

@author: Olufemi Victor Tolulope. @osinkolu on github.
Github repo: https://github.com/osinkolu

"""

from fastai.learner import load_learner #the only thing we need from fastai is its load learner in fastbook
from flask import Flask, request, jsonify # Use Flask to manage ag
import numpy as np
from PIL import Image


#########################
# For us windows users - Redirect poxipath

import pathlib

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

#########################



learn=load_learner("export.pkl")


app = Flask(__name__)
@app.route('/')
def hello_world():
    return("Welcome, This is an API built for the Data Talks Club competition which requires that we classify Kitchen utensils. To test out the API use the /predict endpoint😉")
    

@app.route("/predict", methods=['GET', 'POST'])
def predict():
    try:
        file = request.files['image']
    except Exception:
        return("Could not read any file")

    # Read the image via file.stream
    try:
        im = Image.open(file.stream).convert('RGB')  #convert in case we have a wierd number of channels in the image.
    except Exception:
        return("PIL could not open image from the file stream")
    try:
        im.thumbnail((512, 512), Image.ANTIALIAS)
    except:
        return("PIL could not thumbnail the Image")
    try:
        image_np = np.asarray(im)
    except Exception:
        return("Numpy could not translate image into array")

    result = learn.predict(image_np)
    confidence = round(float(result[2].max())*100,2)

    if confidence > 70.00:
        return jsonify({'msg': 'Success', "confidence":"High","Confidence_value":round(float(result[2].max())*100,2), "Label":result[0]})
    elif confidence > 50:
        return jsonify({'msg': 'Success', "confidence":"Low","Confidence_value":round(float(result[2].max())*100,2), "Label":result[0]})
    else:
        return jsonify({'msg': 'Success', "confidence":"Very Low","Confidence_value":round(float(result[2].max())*100,2), "Label":result[0]})


if __name__ =="__main__":
    app.run(host='0.0.0.0', port=8080)