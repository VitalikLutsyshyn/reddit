from db import db
from datetime import datetime,timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)#autoincrement=True--Автозаповнення
    nickname = db.Column(db.String(100),unique=True,nullable=False)#unique-Унікальне,nullable-має бути текст
    email = db.Column(db.String(150),unique=True,nullable=False)
    gender = db.Column(db.String(20))
    password = db.Column(db.String(300),nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc))#timexone-Враховується часовий пояс,default=datetime.utcnow-передає поточний час
    bio = db.Column(db.Text,nullable=False)
    avatar = db.Column(db.Text,default="man.png")
    user_comments = db.relationship("Comment", backref="comment_author",lazy=True)
    user_topics = db.relationship("Topic",backref="topic_author",lazy=True)
    user_posts = db.relationship("Post",backref = "post_author",lazy=True)

    def hash_password(self,password):#Створення функції шифрування паролю
        self.password = generate_password_hash(password)#Команда для шифрування пароль

    def check_password(self,real_password):#Створення функції для перевірки зашифрованого паролю
        return check_password_hash(self.password,real_password)

    def __repr__(self):#представлення обєкта в програмі
        return f'User {self.nickname}'
    

class Topic(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    author_id = db.Column(db.Integer,db.ForeignKey("user.id"))#Задаємо зовнішній ключ
    name = db.Column(db.String(200),unique=True)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc))
    rules = db.Column(db.String)
    image = db.Column(db.Text,default="photo-circle.png")
    cover = db.Column(db.Text)#Обкладинка
    posts = db.relationship("Post", backref="topic", lazy=True)#Робимо звязок один до багатьох
     

class TopicMember(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)#id підписки
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"),nullable=False)#Задаємо зовнішній ключ
    id_topic = db.Column(db.Integer,db.ForeignKey("topic.id"),nullable = False)#Задаємо зовнішній ключ
    joined_at = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc))#timexone-Враховується часовий пояс,default=datetime.utcnow-передає поточний час

    user = db.relationship("User",backref = "subscriptions")
    topic = db.relationship("Topic", backref = "members")# Учасники обговорення

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    author_id = db.Column(db.Integer,db.ForeignKey("user.id"))#Задаємо зовнішній ключ
    image = db.Column(db.Text)
    topic_id = db.Column(db.Integer,db.ForeignKey("topic.id"))#("topic.id")--посилання
    title = db.Column(db.String(200),)
    content = db.Column(db.Text)
    published_at = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc))
    likes = db.relationship("Like",backref="liked_post",lazy=True)
    comments=db.relationship("Comment", backref="post",lazy=True)
    

class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    post_id = db.Column(db.Integer,db.ForeignKey("post.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    content = db.Column(db.Text)
    # author = db.relationship("User",backref="user_comments",lazy=True)
    published_at = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc))


class Like(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    post_id = db.Column(db.Integer,db.ForeignKey("post.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))