from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_login import LoginManager, UserMixin, login_user,logout_user,current_user,login_required
from sqlalchemy.orm import DeclarativeBase
from config import *
from flask_migrate import Migrate
from db import db

app = Flask(__name__)
app.secret_key = SECRET_KEY

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI  #Створює адресу бази даних 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS #дозволяє відслудковувати зміни в базі даниХ

db.init_app(app)#повязує базу даних з додатком (app)

migrate = Migrate(app,db)#додаємо міграції
from models import User, Topic,Post


@app.route("/")
def index():
   
    return render_template("index.html")


@app.route("/add_user")
def add_user():
    user = User(nickname="Admination",email="administration@gmail.com",gender="male",password="123123123",bio="Heloooo")
    db.session.add(user)#Додаємо користувача в сесію
    db.session.commit()#Збереження(додавання) у базу даних
  
    return f"User {user.nickname} Додано!!!"


@app.route("/add_topic")
def add_topic():
    topic = Topic(name="Games")
    db.session.add(topic)#Додаємо користувача в сесію
    db.session.commit()#Збереження(додавання) у базу даних
    return f"User {topic.name} Додано!!!"

@app.route("/add_post")
def add_post():
    post = Post(title="I've been stuck in an elevator for over an hour",content="Today I got stuck in the elevator and was there for 2 hours. When I got stuck, I was supposed to go out with my friends, but instead I sat in the elevator all that time.")
    db.session.add(post)#Додаємо користувача в сесію
    db.session.commit()#Збереження(додавання) у базу даних
    return f"User {post.title} Додано!!!"

    


if __name__  == "__main__":
    app.run(debug=True)   