from flask import Flask, render_template, redirect, current_app, send_from_directory, url_for, send_file
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_sqlalchemy import SQLAlchemy
from app import app
from app.forms import PictureForm
from werkzeug.utils import secure_filename
import os
import io
import shutil
import zipfile

from predictors.blur_predict import predict_blurry, clear_directory
from predictors.aesthetic_predict import predict_aesthetic

images = UploadSet('images', IMAGES)
configure_uploads(app, images)

@app.route('/')
@app.route('/index')
def index():
    info = {'website_name': 'Photograph Selector'}

    return render_template('index.html', title='Home', info=info)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/submit', methods=['GET','POST'])
def submit():
    form = PictureForm()
    if form.validate_on_submit(): 
        clear_directory('app/static/uploads')
        clear_directory('app/static/accepted')
        clear_directory('app/static/rejected')
        clear_directory('app/static/0')
        clear_directory('app/static/1')
        clear_directory('app/static/2')
        clear_directory('app/static/3')

        for file in form.image.data:
            file_filename = secure_filename(file.filename)
            file.save(os.path.join('app/'+app.config['UPLOAD_FOLDER'],file_filename))
            
        blur = predict_blurry('app/'+app.config['UPLOAD_FOLDER'], 250, (512,512))
        for reject in blur[0]:
            path = 'app/static/rejected'
            shutil.copy(os.path.join('app/'+app.config['UPLOAD_FOLDER'], reject), os.path.join(path, reject))
        for accept in blur[1]:
            path = 'app/static/accepted'
            shutil.copy(os.path.join('app/'+app.config['UPLOAD_FOLDER'], accept), os.path.join(path, accept))

        aesthetic = predict_aesthetic('app/static/accepted')
        for pic in aesthetic[0]:
            path = 'app/static/0'
            shutil.copy(os.path.join('app/'+app.config['UPLOAD_FOLDER'], pic), os.path.join(path,pic))
        for pic in aesthetic[1]:
            path = 'app/static/1'
            shutil.copy(os.path.join('app/'+app.config['UPLOAD_FOLDER'], pic), os.path.join(path,pic))
        for pic in aesthetic[2]:
            path = 'app/static/2'
            shutil.copy(os.path.join('app/'+app.config['UPLOAD_FOLDER'], pic), os.path.join(path,pic))
        for pic in aesthetic[3]:
            path = 'app/static/3'
            shutil.copy(os.path.join('app/'+app.config['UPLOAD_FOLDER'], pic), os.path.join(path,pic))


        return redirect('/results')
    return render_template('submit.html', title='Submit Picture', form=form)

@app.route('/results')
def results():
    accept = os.listdir('app/static/accepted')
    reject = os.listdir('app/static/rejected')
    best = os.listdir('app/static/0')
    great = os.listdir('app/static/1')
    good = os.listdir('app/static/2')
    bad = os.listdir('app/static/3')
    return render_template('results.html', title='Results', accept=accept, reject=reject, best=best, great=great, good=good, bad=bad)

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/download_images')
def download_images():
    folder_path = 'app/static/accepted'
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root,file)
                zipf.write(file_path,os.path.relpath(file_path,folder_path))
    
    zip_buffer.seek(0)
    return send_file(zip_buffer, mimetype='application/zip',as_attachment=True,download_name='accepted_images.zip')

@app.route('/download_0')
def download_images_0():
    folder_path = 'app/static/0'
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root,file)
                zipf.write(file_path,os.path.relpath(file_path,folder_path))
    
    zip_buffer.seek(0)
    return send_file(zip_buffer, mimetype='application/zip',as_attachment=True,download_name='images_best.zip')

@app.route('/download_1')
def download_images_1():
    folder_path = 'app/static/1'
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root,file)
                zipf.write(file_path,os.path.relpath(file_path,folder_path))
    
    zip_buffer.seek(0)
    return send_file(zip_buffer, mimetype='application/zip',as_attachment=True,download_name='images_great.zip')

@app.route('/download_2')
def download_images_2():
    folder_path = 'app/static/2'
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root,file)
                zipf.write(file_path,os.path.relpath(file_path,folder_path))
    
    zip_buffer.seek(0)
    return send_file(zip_buffer, mimetype='application/zip',as_attachment=True,download_name='images_good.zip')

@app.route('/download_3')
def download_images_3():
    folder_path = 'app/static/3'
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root,file)
                zipf.write(file_path,os.path.relpath(file_path,folder_path))
    
    zip_buffer.seek(0)
    return send_file(zip_buffer, mimetype='application/zip',as_attachment=True,download_name='images_bad.zip')