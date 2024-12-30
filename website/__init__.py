from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .password import secret_key,dbpassword
from os import path
from flask_login import LoginManager

badridb=SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='C:\\Users\\badri\\Desktop\\falskproj\\website\\tempalets')#, template_folder='C:\\Users\\badri\\Desktop\\Project\\tempalets'
    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:'+dbpassword+'@127.0.0.1/badridb'

    UPLOAD_FOLDER='static/images/'
    app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

    badridb.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')

    from .database import User,Note

    with app.app_context():
        if not path.exists('website/database.badridb'):
            badridb.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.home'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app



# if __name__ == '__main__':
#     app, badridb = create_app()
#     app.run(debug=True)