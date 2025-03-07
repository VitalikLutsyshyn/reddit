from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,BooleanField,TextAreaField,RadioField,SelectField,TextAreaField,FileField,SubmitField
from wtforms.validators import DataRequired,Length,Email,EqualTo
from flask_wtf.file import FileAllowed

GENDER_CHOICES = [
    ("","Виберіть стать"),
    ("male","Чоловік"),
    ("female","Жінка"),
    ("other","Інше")
]#Список вибору в gender

class RegistrationForm(FlaskForm):
    nickname = StringField("Нікнейм", validators=[DataRequired(),Length(min=4, max=20)])#Створення форми.Validators-це перевірка на правильність,DataRequired()--Перевірка чи заповнене поле   
    email = StringField("Ваш Email",validators=[DataRequired(),Email(),Length(min=4,max=100)])
    gender = SelectField("Ваша Стать",choices=GENDER_CHOICES)
    password = StringField("Пароль",validators=[DataRequired(),Length(min=8)])
    check_password = StringField("Повторіть Пароль",validators=[DataRequired(),Length(min=8),EqualTo("password")])
    bio = TextAreaField("Про вас")
    avatar = FileField("Завантежте аватар",validators=[FileAllowed(["jpg","png","jpeg","webp"],"Виберіть зображення")])  

    submit = SubmitField("Зареєструватися")