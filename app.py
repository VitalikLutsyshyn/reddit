from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_login import LoginManager, UserMixin, login_user,logout_user,current_user,login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from config import *

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.secret_key = SECRET_KEY

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI  #Створює адресу бази даних 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS #дозволяє відслудковувати зміни в базі даних
db.init_app(app)

@app.route("/")
def index():
   

    return render_template("index.html")




if __name__  == "__main__":
    app.run(debug=True)