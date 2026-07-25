from flask import Blueprint, render_template, session,redirect,url_for, abort
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/cabinet/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))

@main.route('/cabinet')
@login_required
def dashboard():
    return render_template('/cabinet/dashboard.html')


