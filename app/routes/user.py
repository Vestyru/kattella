from flask import Blueprint, redirect, render_template, flash, request, url_for
from flask_login import login_user, logout_user, login_required, current_user
from ..extensions import db,bcrypt
from ..forms import LoginForm, RegisterForm
from ..models.user import User
from ..models.quiz import TestResult

user = Blueprint('user', __name__)

@user.route('/cabinet')
@login_required
def cabinet():
    results = TestResult.query.all()
    return render_template('cabinet/dashboard.html', results=results)

@user.route('/cabinet/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, login=form.login.data , email=form.email.data, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(str(e))
            flash(f"При регистрации произошла ошибка")
    return render_template('cabinet/register.html', form=form)


@user.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/cabinet')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.status != 'admin':
                flash('Доступ закрыт!', 'danger')
                return render_template('main/login.html', form=form)

            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Вы успешно авторизовались', 'danger')
            return redirect(next_page) if next_page else redirect('/cabinet')
        else:
            flash('Ошибка входа, проверьте логин или пароль', 'danger')

    return render_template('main/login.html', form=form)

@user.route('/logout',methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect('/login')



