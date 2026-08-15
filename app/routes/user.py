from flask import Blueprint, redirect, render_template, flash, request, session, url_for, current_app, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from is_safe_url import is_safe_url
from sqlalchemy.exc import SQLAlchemyError
from ..extensions import db,bcrypt
from ..forms import LoginForm, RegisterForm,SearchForm, UpdateProfile
from ..models.user import User
from ..models.quiz import TestResult, Participants

user = Blueprint('user', __name__)


@user.route('/cabinet/report/<int:result_id>')
@login_required
def report(result_id):
    result = TestResult.query.get_or_404(result_id)

    if current_user.status != 'admin':
        if current_user.group != result.participant.squad:
            flash('У вас нет доступа к этому отчету', 'danger')
            return redirect('/cabinet')

    return render_template('cabinet/report.html', result=result)


@user.route('/cabinet/register/<int:user_id>/delete')
@login_required
def delete_user(user_id):

    user = User.query.get_or_404(user_id)

    if current_user.status != 'admin':
        flash('У вас недостаточно прав!', 'danger')
        return redirect('/cabinet')
    try:
        db.session.delete(user)
        db.session.commit()
        return redirect('/cabinet/register')
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'success': False}), 500


@user.route('/cabinet', methods=['GET', 'POST'])
@login_required
def cabinet():
    form = SearchForm()

    fullname = request.form.get('fullname') if request.method == 'POST' else request.args.get('fullname', '')
    callsign = request.form.get('callsign') if request.method == 'POST' else request.args.get('callsign', '')
    date = request.form.get('date') if request.method == 'POST' else request.args.get('date', '')

    page = request.args.get('page', 1, type=int)
    per_page = 20

    query = TestResult.query.join(Participants)

    if current_user.group != 'admin':
        if current_user.group:
            query = query.filter(Participants.squad == current_user.group)
        else:
            query = query.filter(False)
            flash('Вам не назначена группа!', 'warning')

    if fullname:
        query = query.filter(Participants.fullname.ilike(f'%{fullname}%'))

    if callsign:
        query = query.filter(Participants.callsign.ilike(f'%{callsign}%'))

    if date:
        query = query.filter(Participants.date == date)

    pagination = query.order_by(TestResult.id.asc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False,
        max_per_page=50,
    )

    offset = (page - 1) * per_page

    return render_template(
        'cabinet/dashboard.html',
        offset=offset,
        pagination=pagination,
        items=pagination.items,
        form=form,
        fullname=fullname or '',
        callsign=callsign or '',
        date=date or '',
    )


@user.route('/cabinet/register', methods=['GET', 'POST'])
@login_required
def register():

    if current_user.status != "admin":
        flash('Доступ закрыт!', 'danger')
        return redirect('/cabinet')

    form = RegisterForm()

    groups = db.session.query(Participants.squad).distinct().all()
    group_choices = [(g.squad, g.squad) for g in groups if g.squad]
    group_choices.insert(0, ('admin', 'Все группы'))
    form.group_user.choices = group_choices

    form.group_status.choices = [
        ('admin', 'Администратор'),
        ('moderator', 'Модератор'),
    ]

    group_users = User.query.order_by(User.date).all()

    group = form.group_user.data
    if group == 'admin':
        group = 'admin'

    password = form.password.data
    password2 = form.password2.data

    if password != password2:
        flash('Пароли не совпадают', 'danger')
        return render_template('/cabinet/_register.html',form=form,group_users=group_users)

    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(full_name=form.full_name.data,name=form.name.data, login=form.login.data , email=form.email.data, password=hashed_password, group=group,status=form.group_status.data)
        try:
            db.session.add(user)
            db.session.commit()
            next_page = request.args.get('next')

            if next_page and is_safe_url(next_page, request.host_url):
                return redirect(next_page)

            return redirect(url_for("user.cabinet"))
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.exception(e)
            flash(f"При регистрации произошла ошибка")
    return render_template('cabinet/_register.html', form=form,group_users=group_users)



@user.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect('/cabinet')

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.status not in ("admin", "moderator"):
                flash('Доступ закрыт!', 'danger')
                return render_template('main/login.html', form=form)

            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")

            if next_page and is_safe_url(next_page, request.host_url):
                return redirect(next_page)

            flash('Вы успешно авторизовались', 'success')
            return redirect(url_for("user.cabinet"))
        else:
            flash('Неверный логин или пароль', 'danger')

    return render_template('main/login.html', form=form)


@user.route('/cabinet/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = UpdateProfile()

    if form.validate_on_submit():
        user = User.query.get_or_404(current_user.id)

        if form.password.data:
            if not bcrypt.check_password_hash(user.password, form.password.data):
                flash('Неверный текущий пароль!', 'danger')
                return render_template('cabinet/_settings.html', form=form)


        user.name = form.name.data

        if form.password1.data:
            user.password = bcrypt.generate_password_hash(form.password1.data).decode('utf-8')

        try:
            db.session.commit()
            flash('Данные обновлены!', 'success')
            return redirect(url_for('user.settings'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Ошибка сохранения: {str(e)}', 'danger')

    return render_template('cabinet/_settings.html', form=form)


@user.route('/logout',methods=['GET'])
def logout():
    logout_user()
    session.clear()
    return redirect('/login')



