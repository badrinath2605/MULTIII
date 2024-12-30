from flask import Blueprint,render_template,request,flash,redirect,url_for,jsonify,session
from .database import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import badridb   #means from __init__.py import db
# from flask_mysqldb import MySQL
import subprocess




auth=Blueprint('auth',__name__)
# app = Flask(__name__, template_folder='C:\\Users\\badri\\Desktop\\flaskproj\\tempalets')
# app.secret_key=

# app.config['MYSQL_HOST']="127.0.0.1"
# app.config['MYSQL_USER']='root'
# app.config['MYSQL_PASSWORD']=""
# app.config['MYSQL_DB']="badridb"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
# mysql = MySQL(app)

# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT']=465
# app.config['MAIL_USERNAME']='mul.multiii@gmail.com'
# app.config['MAIL_PASSWORD']='mulmulmul'
# app.config['MAIL_USE_TLS']=False
# app.config['MAIL_USE_SSL']=True
# mail=Mail(app)

@auth.route('/home')
@auth.route('/')
def home():
    return render_template("home.html")

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        email= request.form.get('Email')
        password = request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
            if(check_password_hash(user.password,password)):
                # return redirect(url_for('views.login_home'))
                flash("Logged in successfully!",category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.login_home'))
            else:
                flash('Incorrect password, try again',category='error')
        else:
            flash('Email is not registered.', category='error')
    return render_template("login.html")

@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method=="POST":

        full_name= request.form.get('Full Name')
        username= request.form.get('Username')
        email=request.form.get('Email')
        password=request.form.get('password')
        password_conform=request.form.get('password_conform')
        user=User.query.filter_by(email=email).first()
        # code_c = random.randint(1, 10)
        # print(code_c)
        # data=request.form
        # print(data)
        #print(full_name,username,email,password,password_conform)
        if user:
            flash('Email already exists.',category='error')
        elif len(email)<4:
           flash('Email msut be greater than 4 characters',category='error')
        elif len(full_name)<2:
            flash('full name msut be greater than 2 characters',category='error')
        elif len(username)<3:
            flash('username must be greter than 3 characters',category='error')
        elif (password!=password_conform):
             flash('Password doesn\'t Match!!! Try Again',category='error')
        else:
            new_user=User(email=email,password=generate_password_hash(password,method='pbkdf2:sha256'),full_name=full_name,username=username)
            badridb.session.add(new_user)
            badridb.session.commit()   
            flash('Account created!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.login_home'))
            # try:
            # msg=Message("hey",sender="badrinathachanta@demo.com",recipients=["mul.multiii@gmail.com"])
            # msg.body="hey how r u "
            # #mail.send(msg)
            # code=request.form.get('code')
            # if(code==code_c):
    return render_template("signup.html")

@auth.route('/Logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.home'))
