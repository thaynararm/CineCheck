import os


SECRET_KEY = 'fitdance'

SQLALCHEMY_DATABASE_URI = '{SGBD}://{user}:{password}@{host}:{port}/{database}'.format(
    SGBD='mysql+mysqlconnector',
    user='root',
    password='065Karla030*',
    host='localhost',
    port='3306',
    database='cinecheck'
    )

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
