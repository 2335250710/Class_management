import os


from flask import Flask

from views.login import logins
from views.grade import grades
from views.student import students
from views.permission import permissions
from views.user import users


def create_app():
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(BASE_DIR, 'static')
    templates_dir = os.path.join(BASE_DIR, 'templates')

    app = Flask(__name__,
                static_folder=static_dir,
                template_folder=templates_dir)
    app.register_blueprint(blueprint=logins, url_prefix='/user')
    app.register_blueprint(blueprint=grades, url_prefix='/user')
    app.register_blueprint(blueprint=students, url_prefix='/user')
    app.register_blueprint(blueprint=permissions, url_prefix='/user')
    app.register_blueprint(blueprint=users, url_prefix='/user')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/Htai'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 设置session密钥
    app.config['SECRET_KEY'] = 'secret_key'


    return app
