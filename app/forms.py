from flask_wtf import FlaskForm
from .models.user import User
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, length, ValidationError


class RegisterForm(FlaskForm):
    name = StringField("ФИО", validators=[DataRequired(), length(min=7, max = 90)])
    email = StringField('email', validators=[DataRequired(), length(min=7, max = 30)])
    login = StringField('Логин', validators=[DataRequired(), length(min=5, max = 16)])
    password = PasswordField('Пароль', validators=[DataRequired(), length(min=7, max = 30)])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), length(min = 7, max = 30)])
    submit = SubmitField('Зарегистрировать')

    def validate_login(self, login):
        user = User.query.filter_by(login = login.data).first()
        if user:
            raise ValidationError('Имя пользователя занято. Пожалуйста, выберите другое')

class TestForm(FlaskForm):
    fullname = StringField('ФИО', validators=[DataRequired(),length(min=7, max = 30)])
    squad = StringField('Ваш позывной', validators=[DataRequired(),length(min=2, max = 8)])
    callsign = StringField('Отряд', validators=[DataRequired(),length(min=2, max = 20)])
    date = StringField('Дата рождения', validators=[DataRequired()])
    submit = SubmitField('Начать тест')


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(), length(min=3, max = 30)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
