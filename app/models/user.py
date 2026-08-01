from datetime import datetime
from ..extensions import  db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(50))
    login = db.Column(db.String(50))
    email = db.Column(db.String(120))
    password = db.Column(db.String(255))
    status = db.Column(db.String, default='user')
    group = db.Column(db.String(255), nullable=True, default=None)
    date = db.Column(db.DateTime,default=datetime.utcnow)

    def has_group_access(self, group_name):
        if self.status == 'admin':
            return True
        return self.group == group_name