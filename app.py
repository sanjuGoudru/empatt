# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 11:48:14 2021

@author: Sanjay G R
"""

import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory,render_template
from werkzeug.utils import secure_filename
import pandas as pd
import pickle


UPLOAD_FOLDER = r"F:\My_ML_Projects\Final Year Project\empatt\uploads"
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def check_for_attributes(filename):
    df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    print("Database length:",len(df.columns))
    if len(df.columns) != 34:
        return False
    return True

def get_cols_to_be_dropped(preprocess_dict):
    cols_to_be_dropped = []
    for col in preprocess_dict['onehot_encoded_features']:
        item = col+'_'+list(preprocess_dict['onehot_dropped_col_dict'][col])[0]
        cols_to_be_dropped.append(item)
    return cols_to_be_dropped

def preprocess_file(filename):
    df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    preprocess_dict = pickle.load(open('preprocess_dict','rb'))
    df = df.drop(labels=preprocess_dict['rem_constant_features'],axis=1)
    df['BusinessTravel'] = df['BusinessTravel'].map(preprocess_dict['BusinessTravel'])
    df = pd.get_dummies(df,columns=preprocess_dict['onehot_encoded_features'])
    cols_to_be_dropped = get_cols_to_be_dropped(preprocess_dict)
    df = df.drop(labels=cols_to_be_dropped,axis=1)
    return df

def predict_attrition(df):
    stk_clr = pickle.load(open('stk_final1','rb'))
    preds = stk_clr.predict(df)
    return preds

@app.route('/', methods=['POST','GET'])
def home():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            is_accurate = check_for_attributes(filename)
            if not is_accurate:
                return "Unsuccessful"
            df = preprocess_file(filename)
            predictions = predict_attrition(df)
            s = ""
            for p in predictions:
                s+= (str(p)+"\n")
            return s
    return render_template('home.html')

    
@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)
