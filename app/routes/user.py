from flask import Blueprint, redirect, render_template, flash, request,session
from flask_login import login_user, logout_user, login_required, current_user
from ..extensions import db,bcrypt
from ..forms import LoginForm, RegisterForm,SearchForm
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


@user.route('/cabinet/settings')
@login_required
def settings():

    return render_template('cabinet/_settings.html')


@user.route('/cabinet', methods=['GET', 'POST'])
@login_required
def cabinet():
    form = SearchForm()

    fullname_q = request.form.get('fullname') if request.method == 'POST' else request.args.get('fullname', '')
    callsign_q = request.form.get('callsign') if request.method == 'POST' else request.args.get('callsign', '')
    date_q = request.form.get('date') if request.method == 'POST' else request.args.get('date', '')

    page = request.args.get('page', 1, type=int)
    per_page = 20

    query = TestResult.query.join(Participants)

    if current_user.status != 'admin':
        if current_user.group:
            query = query.filter(Participants.squad == current_user.group)
        else:
            query = query.filter(False)
            flash('Вам не назначена группа!', 'warning')

    if fullname_q:
        query = query.filter(Participants.fullname.ilike(f'%{fullname_q}%'))

    if callsign_q:
        query = query.filter(Participants.callsign.ilike(f'%{callsign_q}%'))

    if date_q:
        query = query.filter(Participants.date == date_q)

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
        fullname_q=fullname_q or '',
        callsign_q=callsign_q or '',
        date_q=date_q or '',
    )


@user.route('/cabinet/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegisterForm()

    form.group_user.choices = [(g.squad, g.squad) for g in db.session.query(Participants.squad).distinct().all() if g.squad]
    form.group_status.choices = [(g.status, g.status) for g in db.session.query(User.status).distinct().all() if g.status]

    group_users = User.query.all()


    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, login=form.login.data , email=form.email.data, password=hashed_password, group=form.group_user.data,status=form.group_status.data)
        try:
            db.session.add(user)
            db.session.commit()
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/cabinet')
        except Exception as e:
            print(str(e))
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
            if user.status != 'admin' and user.status != 'moderator':
                flash('Доступ закрыт!', 'danger')
                return render_template('main/login.html', form=form)

            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Вы успешно авторизовались', 'danger')
            return redirect(next_page) if next_page else redirect('/cabinet')
        else:
            flash('Ошибка входа, проверьте логин или пароль', 'danger')

    return render_template('main/login.html', form=form)

@user.route('/logout',methods=['GET'])
def logout():
    logout_user()
    session.clear()
    return redirect('/login')



