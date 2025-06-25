#підключення всіх функцій
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify  # Імпорт Flask-функцій для створення веб-додатку
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required  # Імпорт функцій для авторизації
from sqlalchemy.orm import DeclarativeBase  # Для створення базової моделі SQLAlchemy
from sqlalchemy import func
from config import *  # Імпорт налаштувань (наприклад, секретного ключа, URI бази тощо)
from flask_migrate import Migrate  # Для керування міграціями бази даних
from db import db  # Імпорт об’єкта бази даних
from werkzeug.utils import secure_filename  # Для безпечного збереження імен файлів
from forms import RegistrationForm, LoginForm, PostForm, TopicForm, CommentForm  # Імпорт форм (реєстрації, входу, посту, топіка)
import os  # Робота з файловою системою
from datetime import datetime, timezone, timedelta
app = Flask(__name__)  # Створення екземпляру Flask-додатку
app.secret_key = SECRET_KEY  # Встановлення секретного ключа

login_manager = LoginManager()  # Створення менеджера логіну
login_manager.init_app(app)  # Ініціалізація логін-менеджера з Flask-додатком
login_manager.login_view = "login"  # Встановлення маршруту для редиректу при необхідності входу

app.config["CSRF_ENABLED"] = True  # Увімкнення CSRF-захисту
app.config["UPLOAD_FOLDER"] = "static/users_uploads"  # Шлях для завантаження файлів користувачами

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI  # URI для підключення до бази даних
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS  # Вимикає відслідковування змін моделей (рекомендується)

db.init_app(app)  # Ініціалізує базу даних із додатком

migrate = Migrate(app, db)  # Ініціалізує Flask-Migrate для керування міграціями
from models import User, Topic, Post, Comment, Like,TopicMember  # Імпорт моделей користувача, тем і постів

@login_manager.user_loader
def load_user(user_id):  # Функція завантаження користувача за ID (використовується Flask-Login)
    return User.query.get(int(user_id))

@app.route("/")
def index():  # Головна сторінка
    days_ago = datetime.now(timezone.utc) - timedelta(days=14)
    posts = Post.query.filter(Post.published_at>=days_ago).all()
    return render_template("index.html",posts = posts)  # Рендеринг шаблону index.html


############################################
@app.route("/popular")
def popular():  # Головна сторінка
    posts = Post.query.all()
    posts = sorted(posts, key= lambda post:len(post.likes))
    return render_template("index.html",posts = posts)  # Рендеринг шаблону index.html
#################################################


@app.route("/favicon.ico/")
def favicon():
    return redirect(url_for('static', filename = "favicon.ico"))

@app.route("/registration", methods=["POST", "GET"])
def user_registration():  # Сторінка реєстрації
    form = RegistrationForm()  # Створення форми реєстрації
    if form.validate_on_submit():  # Перевірка чи форма валідна
        is_user = User.query.filter_by(nickname=form.nickname.data).first()  # Перевірка чи існує нікнейм
        is_email = User.query.filter_by(email=form.email.data).first()  # Перевірка чи існує email

        if is_user:
            flash("Введіть інше нік.Такий нік вже існує", "alert-warning")  # Повідомлення про помилку
        elif is_email:
            flash("Введіть інший email.Такий email вже існує", "alert-warning")
        elif form.password.data != form.check_password.data:  # Перевірка паролів
            flash("Паролі мають бути одинакoві", "alert-warning")
        else:
            if form.avatar.data:  # Якщо додано аватар
                avatar_file = form.avatar.data
                filename = secure_filename(avatar_file.filename)  # Безпечне ім’я файлу
                path = os.path.join(app.config["UPLOAD_FOLDER"], filename)  # Шлях до збереження
                avatar_file.save(path)  # Збереження файлу
            else:
                filename = "man.png"  # Аватар за замовчуванням

            user = User(  # Створення користувача
                nickname=form.nickname.data,
                email=form.email.data,
                gender=form.gender.data,
                password=form.password.data,
                bio=form.bio.data,
                avatar=filename
            )
            user.hash_password(user.password)  # Хешування пароля
            db.session.add(user)  # Додавання до сесії БД
            db.session.flush()  # Проміжне збереження, щоб отримати user.id

            user_topic = Topic(author_id=user.id, name=user.nickname)  # Тема користувача за замовчуванням
            db.session.add(user_topic)  # Додавання теми

            db.session.commit()  # Остаточне збереження у базі
            login_user(user)  # Авторизація користувача
            return redirect(url_for("index"))  # Перехід на головну
    return render_template("registration.html", form=form)  # Відображення форми

@app.route("/login", methods=["POST", "GET"])
def login():  # Сторінка входу
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # Пошук користувача за email
        if user:
            if user.check_password(form.password.data):  # Перевірка пароля
                login_user(user)  # Вхід користувача
                return redirect(url_for("index"))  # Перехід на головну
            else:
                flash("Ви ввели неправильний email або пароль", "alert-warning")
        else:
            flash("Ви ввели неправильний email або пароль", "alert-warning")
    return render_template("login.html", form=form)  # Відображення форми

@app.route("/logout")
@login_required  # Доступ тільки для авторизованих
def logout():
    logout_user()  # Вихід користувача
    flash("Ви вийшли з профілю", "alert-primary")
    return redirect(url_for("login"))  # Повернення на сторінку входу

@app.route("/<topic_name>/add_post", methods=["POST", "GET"])
@login_required
def add_post(topic_name):  # Додавання посту
    form = PostForm()
    topic = Topic.query.filter_by(name = topic_name).first()

    if form.validate_on_submit():
        if form.image.data:  # Якщо завантажено зображення
            image = form.image.data
            filename = secure_filename(image.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image.save(path)
        else:
            filename = ""

        post = Post(  # Створення посту
            title=form.title.data,
            content=form.content.data,
            image=filename,
            author_id=current_user.id,
            topic_id= topic.id)
        
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("topic_page",topic_name = topic_name))
    
    return render_template("add_post.html", form=form)


@app.route("/add_topic", methods=["POST", "GET"])
@login_required
def add_topic():  # Додавання нової теми
    form = TopicForm()
    if form.validate_on_submit():
        is_topic = Topic.query.filter_by(name=form.name.data).first()  # Перевірка чи тема існує
        if is_topic:
            flash("Такий топік вже існує", "alert-warning")
            return redirect(url_for("add_topic"))

        if form.image.data:  # Завантаження картинки теми
            image = form.image.data
            filename = secure_filename(image.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image.save(path)
        else:
            filename = "photo-circle.png"

        if form.image.data:  # Завантаження обкладинки теми
            cover = form.cover.data
            cover_filename = secure_filename(cover.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"], cover_filename)
            cover.save(path)
        else:
            cover_filename = ""

        topic = Topic(  # Створення теми
            name=form.name.data,
            image=filename,
            cover=cover_filename,
            rules=form.rules.data,  
            author_id=current_user.id
        )
        db.session.add(topic)
        db.session.commit()

        return redirect(url_for("topic_page",topic_name = topic.name))
    return render_template("add_topic.html", form=form)


@app.route("/<topic_name>/")#Буде підписуватися назва топіка в url адресі
def topic_page(topic_name):
    topic = Topic.query.filter_by(name=topic_name).first()
    subscribed = False
    if current_user.is_authenticated:
        is_subscribe = TopicMember.query.filter_by(id_topic=topic.id, id_user=current_user.id).first()
        if is_subscribe:
            subscribed = True


    return render_template("topic_page.html",topic=topic, subscribed = subscribed) 

@app.route("/like/<int:post_id>")
@login_required
def post_like(post_id):
    post = Post.query.get_or_404(post_id)
    is_like = Like.query.filter_by(post_id=post_id,user_id= current_user.id).first()
    if is_like:
        db.session.delete(is_like)
        db.session.commit()
    else:
        new_like = Like(post_id=post_id,user_id= current_user.id)
        db.session.add(new_like)
        db.session.commit()
    return jsonify({"likes": len(post.likes)})

@app.route("/<topic_name>/<int:post_id>", methods = ["POST","GET"])
def post_page(topic_name,post_id):
    post = Post.query.get(post_id)
    form =  CommentForm()

    post_liked = False
    if current_user.is_authenticated:
        is_like = Like.query.filter_by(post_id=post_id,user_id= current_user.id).first()
        if is_like:
            post_liked = True
            

    if form.validate_on_submit():
        if current_user.is_authenticated:
            comment = Comment(post_id=post_id,
                            user_id=current_user.id,
                            content=form.content.data
                            )
            db.session.add(comment)
            db.session.commit()
        else:   
            flash("Увійдіть щоб залишити коментар","alert-warning")

    return render_template("post_page.html",post=post,form=form, post_liked = post_liked)


##################################################33
@app.route("/subscribe/<int:topic_id>")
@login_required
def subscribe(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    is_subscribe = TopicMember.query.filter_by(id_topic=topic.id, id_user=current_user.id).first()
    if is_subscribe:
        db.session.delete(is_subscribe)
        db.session.commit()
        subscribed = False
    else:
        new_subscibe = TopicMember(id_topic= topic.id,id_user= current_user.id)
        db.session.add(new_subscibe)
        db.session.commit()
        subscribed = True
    



    return jsonify({"subscribed":subscribed})

if __name__ == "__main__":
    app.run(debug=True)  # Запуск додатку в режимі розробки
