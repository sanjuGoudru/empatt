# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 11:48:14 2021

@author: Sanjay G R
"""

import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory,render_template
from werkzeug.utils import secure_filename
import pandas as pd
UPLOAD_FOLDER = r"F:\My_ML_Projects\Final Year Project\empatt\uploads"
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def check_for_attributes(filename):
    df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    print("Database length:",len(df.columns))
    if len(df.columns) != 35:
        return False
    return True


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
            if is_accurate:
                return "Successful"
            else:
                return "Unsuccessful"
    return render_template('home.html')

    
@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)
