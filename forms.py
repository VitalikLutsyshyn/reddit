from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,BooleanField,TextAreaField,RadioField,SelectField,TextAreaField,FileField,SubmitField,PasswordField
from wtforms.validators import DataRequired,Length,Email,EqualTo
from flask_wtf.file import FileAllowed

GENDER_CHOICES = [
    ("","Виберіть стать"),
    ("male","Чоловік"),
    ("female","Жінка"),
    ("other","Інше")
]#Список вибору в gender
#Створення форми для регістрації
class RegistrationForm(FlaskForm):
    nickname = StringField("Нікнейм", validators=[DataRequired(),Length(min=4, max=20)])#Створення форми.Validators-це перевірка на правильність,DataRequired()--Перевірка чи заповнене поле   
    email = StringField("Ваш Email",validators=[DataRequired(),Email(),Length(min=4,max=100)])
    gender = SelectField("Ваша Стать",choices=GENDER_CHOICES)
    password = PasswordField("Пароль",validators=[DataRequired(),Length(min=8)])
    check_password = PasswordField("Повторіть Пароль",validators=[DataRequired(),Length(min=8),EqualTo("password")])
    bio = TextAreaField("Про вас")
    avatar = FileField("Завантежте аватар",validators=[FileAllowed(["jpg","png","jpeg","webp"],"Виберіть зображення")])  

    submit = SubmitField("Зареєструватися")

#Створення форми для логіну
class LoginForm(FlaskForm):
    email = StringField("Email який ви вказували при реєстрації",validators=[DataRequired(),Email(),Length(min=4,max=100)])
    password = PasswordField("Введіть ваш пароль",validators=[DataRequired(),Length(min=8)])

    submit = SubmitField("Увійти")

#Створення форми для постів
class PostForm(FlaskForm):
    title = StringField("Назва",validators=[DataRequired(),Length(min=2,max=200)])
    content = TextAreaField("Що ви хочете розповісти")
    image = FileField("Виберіть картинку",validators=[FileAllowed(["jpg","png","jpeg","webp"],"Виберіть зображення")])

    submit = SubmitField("Опублікувати")

#Створення форми для Топіка
class TopicForm(FlaskForm):
    name = StringField("Назва топіка",validators=[DataRequired(),Length(min=2,max=200)])
    rules = TextAreaField("Правила для топіка")
    image = FileField("Виберіть картинку",validators=[FileAllowed(["jpg","png","jpeg","webp"],"Виберіть зображення")])
    cover = FileField("Додайте обкладинку",validators=[FileAllowed(["jpg","png","jpeg","webp"],"Виберіть зображення")])

    submit = SubmitField("Опублікувати")

class CommentForm(FlaskForm):
    content = TextAreaField("Поділися своїми думками")

    submit = SubmitField("Поділитися")