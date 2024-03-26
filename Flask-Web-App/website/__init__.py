from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
import os

# Initialize database
db = SQLAlchemy()
DB_NAME = "database.db"  # Name of the database


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhbhgf kjshkjdhjs'  # Generate a secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # Location of the database
    db.init_app(app)  # Initialize database using the Flask app we created

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.route('/static/images/<path:path>')
    def send_image(path):
        return send_from_directory(os.path.join(app.root_path, 'static', 'images'), path)

    @app.route('/static/videos/<filename>')
    def send_video(filename):
        return send_from_directory('static/videos', filename)

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
