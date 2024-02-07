from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

# creating database instance
db = SQLAlchemy()
DB_NAME = "database.db"

# main application
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'QhlNilSNaa12nenmsKOi32MMMzn29138'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # initializing database
    db.init_app(app)

    # assigning routes
    from .routes import routes
    app.register_blueprint(routes, url_prefix='/') 

    # making sure database is created
    from .models import Profile
    create_database(app)

    return app

def create_database(app):
    if not path.exists('application/' + DB_NAME):
        with app.app_context():    # i dont understand, what is this for?
            db.create_all() 
        print('Created Database!')