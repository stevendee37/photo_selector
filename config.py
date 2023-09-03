import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'password'
    UPLOADED_IMAGES_DEST = 'static/uploads/'
    UPLOAD_FOLDER = 'static/uploads/'