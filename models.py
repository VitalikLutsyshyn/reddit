from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100),unique=True,nullable=False)#unique-Унікальне,nullable-має бути текст
    email = db.Column(db.String(150),unique=True,nullable=False)
    gender = db.Column(db.String(20))
    password = db.Column(db.String(50),nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)#timexone-Враховується часовий пояс,default=datetime.utcnow-передає поточний час
    bio = db.Column(db.Text,nullable=False)
    

    def __repr__(self):#представлення обєкта в програмі
        return f'User {self.nickname}'
    

class Topics(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text,unique=True,nullable=True)
    posts = db.Column(db.Text,nallable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)


class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=True)
    story = db.Column(db.Text,nullable=True)
    user_nickname = db.Column(db.String(100),unique=True,nullable=True)
    published_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    likes = db.Column(db.Integer,nullable=True)
    rules = db.Column(db.String)
    
class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    comment = db.Column(db.Text,nullabele=True)
    likes = db.Column(db.Integer,nullable=True)
    user_nickname = db.Column(db.String,nullable=True)
    published_at = db.Column(db.DataTime(timezone=True), default=datetime.utcnow)

#таблиці на дз Subreddit,Post,Comment
