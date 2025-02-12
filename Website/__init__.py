from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, makedirs #
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'FUN AI'

    basedir = path.abspath(path.dirname(__file__)) #
    instance_path = path.join(basedir, 'instance') #
    DB_PATH = path.join(instance_path, DB_NAME)  #
    
    if not path.exists(instance_path):  #
        makedirs(instance_path)  #

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}' #DB_NAME TO DB_PATH
    db.init_app(app) 

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = u"Log In Required"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    basedir = path.abspath(path.dirname(__file__)) #
    instance_path = path.join(basedir, 'instance') #
    DB_PATH = path.join(instance_path, DB_NAME) #

    if not path.exists('Website/' + DB_PATH): #
        with app.app_context():
            db.create_all()
            print(' * Created Database!')
