#підключення всіх функцій
from flask import Flask, render_template, request, session, redirect, url_for, flash  # Імпорт Flask-функцій для створення веб-додатку
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required  # Імпорт функцій для авторизації
from sqlalchemy.orm import DeclarativeBase  # Для створення базової моделі SQLAlchemy
from config import *  # Імпорт налаштувань (наприклад, секретного ключа, URI бази тощо)
from flask_migrate import Migrate  # Для керування міграціями бази даних
from db import db  # Імпорт об’єкта бази даних
from werkzeug.utils import secure_filename  # Для безпечного збереження імен файлів
from forms import RegistrationForm, LoginForm, PostForm, TopicForm  # Імпорт форм (реєстрації, входу, посту, топіка)
import os  # Робота з файловою системою

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
from models import User, Topic, Post  # Імпорт моделей користувача, тем і постів

@login_manager.user_loader
def load_user(user_id):  # Функція завантаження користувача за ID (використовується Flask-Login)
    return User.query.get(int(user_id))

@app.route("/")
def index():  # Головна сторінка
    return render_template("index.html")  # Рендеринг шаблону index.html

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

@app.route("/add_post", methods=["POST", "GET"])
@login_required
def add_post():  # Додавання посту
    form = PostForm()
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
            topic_id=current_user.user_topics[0].id  # Прив'язка до теми користувача
        )
        db.session.add(post)
        db.session.commit()
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
            filename = ""

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
    return render_template("add_topic.html", form=form)


@app.route("/<topic_name>/")#Буде підписуватися назва топіка в url адресі
def topic_page(topic_name):
    topic = Topic.query.filter_by(name=topic_name).first()

    return render_template("topic_page.html",topic=topic) 



if __name__ == "__main__":
    app.run(debug=True)  # Запуск додатку в режимі розробки
