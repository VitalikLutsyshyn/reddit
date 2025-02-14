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
    
#таблиці на дз Subreddit,Post,Comment
