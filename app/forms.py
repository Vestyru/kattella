from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from .models.user import User
from wtforms import StringField, SubmitField, PasswordField, BooleanField,DateField
from wtforms.validators import DataRequired, length, ValidationError,Optional


class RegisterForm(FlaskForm):
    full_name = StringField('Личный номер', validators=[DataRequired(), length(min = 10, max = 30)])
    name = StringField("Должность", validators=[DataRequired(), length(min=7, max = 90)])
    email = StringField('email', validators=[DataRequired(), length(min=7, max = 30)])
    login = StringField('Логин', validators=[DataRequired(), length(min=5, max = 16)])
    password = PasswordField('Пароль', validators=[DataRequired(), length(min=7, max = 30)])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), length(min = 7, max = 30)])
    group_user = SelectField('Выберите группу', choices=[], render_kw={"class": "auth-form__input"})
    group_status = SelectField('Выберите статус', choices=[], render_kw={"class": "auth-form__input"})
    submit = SubmitField('Зарегистрировать')

    def validate_login(self, login):
        user = User.query.filter_by(login = login.data).first()
        if user:
            raise ValidationError('Имя пользователя занято. Пожалуйста, выберите другое')


class TestForm(FlaskForm):
    fullname = StringField('Личный номер', validators=[DataRequired(),length(min=7, max = 9)])
    squad = StringField('Отряд', validators=[DataRequired(),length(min=2, max = 8)])
    callsign = StringField('Ваш позывной', validators=[DataRequired(),length(min=2, max = 20)])
    date = StringField('Дата рождения', validators=[DataRequired()])
    submit = SubmitField('Начать тест')


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(), length(min=3, max = 30)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class SearchForm(FlaskForm):
    fullname = StringField('Личный номер', validators=[Optional()])
    callsign = StringField('Позывной', validators=[Optional()])
    date = DateField('Дата рождения', validators=[Optional()])
    submit = SubmitField('Найти')


class Update_profile(FlaskForm):
    full_name = StringField('Личный номер', validators=[DataRequired(), length(min = 10, max = 30)])
    name = StringField('Должность', validators=[DataRequired()])
    login = StringField('Логин', validators=[DataRequired()])
    email = StringField('email')
    password = PasswordField('Текущий пароль', validators=[DataRequired()])
    password1 = PasswordField('Новый пароль', validators=[DataRequired()])
    password2 = PasswordField('Подтвердите новый пароль', validators=[DataRequired()])
    submit = SubmitField('Сохранить изменения')