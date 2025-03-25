from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_login import LoginManager, UserMixin, login_user,logout_user,current_user,login_required
from sqlalchemy.orm import DeclarativeBase
from config import *
from flask_migrate import Migrate
from db import db
from werkzeug.utils import secure_filename
from forms import RegistrationForm,LoginForm,PostForm
import os

app = Flask(__name__)
app.secret_key = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

app.config["CSRF_ENABLED"]=True #Вмикає CSRF захист(Від атак)
app.config["UPLOAD_FOLDER"] = "static/users_uploads"#Файли збережені користувачами

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI  #Створює адресу бази даних 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS #дозволяє відслудковувати зміни в базі даниХ

db.init_app(app)#повязує базу даних з додатком (app)

migrate = Migrate(app,db)#додаємо міграції
from models import User, Topic,Post

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))#Функція яка загружає поточного користувача


@app.route("/")
def index():
   
    return render_template("index.html")


@app.route("/registration",methods=["POST","GET"])
def user_registration():
    form = RegistrationForm()#Створення форми
    if form.validate_on_submit():#Якщо форма пройшла всі перевірки
        if form.avatar.data:#Перевірка чи є аватар
            avatar_file = form.avatar.data#отримуємо файл з аватаром
            filename = secure_filename(avatar_file.filename)#Дістаєм файл щоб безпечно отримати назву
            path = os.path.join(app.config["UPLOAD_FOLDER"],filename)#Прописуємо шлях для збереженя в папку user uploads
            avatar_file.save(path)#Зберігання файлу
        else:
            filename = "man.png"


        user = User(nickname = form.nickname.data,
                    email = form.email.data,
                    gender = form.gender.data,
                    password = form.password.data,
                    bio = form.bio.data,
                    avatar = filename)#Створення рядка в базі даних 

        user.hash_password(user.password)#Шифруємо пароль
        db.session.add(user)#Додаємо користувача в сесію
        db.session.flush()

        user_topic = Topic(author_id = user.id,name = user.nickname)
        db.session.add(user_topic)


        db.session.commit()#Збереження(додавання) у базу даних
        login_user(user)
        return redirect(url_for("index"))
    return render_template("registration.html",form=form)



@app.route("/login",methods=["POST","GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()#Перевірка чи є такий користувач за його email
        if user:
            if user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for("index"))
            
            else:
                flash("Ви ввели неправильний email або пароль","alert-warning")

        else:
            flash("Ви ввели неправильний email або пароль","alert-warning")


    return render_template("login.html",form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Ви вийшли з профілю","alert-primary")
    return redirect(url_for("login"))



@app.route("/add_topic")
def add_topic():
    topic = Topic(name="Games")
    db.session.add(topic)#Додаємо користувача в сесію
    db.session.commit()#Збереження(додавання) у базу даних
    return f"User {topic.name} Додано!!!"


@app.route("/add_post",methods=["POST","GET"])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():#Якщо форма пройшла всі перевірки
        if form.image.data:#Перевірка чи є аватар
            image = form.image.data#отримуємо файл з аватаром
            filename = secure_filename(image.filename)#Дістаєм файл щоб безпечно отримати назву
            path = os.path.join(app.config["UPLOAD_FOLDER"],filename)#Прописуємо шлях для збереженя в папку user uploads
            image.save(path)#Зберігання файлу
        else:
            filename = ""


        post = Post(title =form.title.data,
                    content = form.content.data,
                    image = filename,
                    author_id = current_user.id,
                    topic_id = current_user.user_topics[0].id
                    )

        db.session.add(post)#Додаємо користувача в сесію
        db.session.commit()#Збереження(додавання) у базу даних
    return render_template("add_post.html",form=form)


if __name__  == "__main__":
    app.run(debug=True)   