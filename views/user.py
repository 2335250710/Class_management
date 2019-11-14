from flask import Blueprint, render_template, request, redirect, url_for
from models.models import *
from utils.ch_login import *

users = Blueprint('users', __name__)


@users.route('/userlist/', methods=['GET', 'POST'])
@is_login
def userlist():
    page = int(request.args.get('page', 1))
    paginate = User.query.paginate(page, 5, False)
    users = paginate.items
    return render_template('users.html', paginate=paginate, users=users)


@users.route('/assignrole/', methods=['GET', 'POST'])
@is_login
def assignrole():
    u_id = request.args.get('u_id')
    roles = Role.query.all()
    Users = User.query.filter_by(u_id=u_id).first()
    if request.method == 'POST':
        r_id = request.form.get('r_id')
        Users.role_id = r_id
        db.session.commit()
        return render_template('assign_user_role.html', msg='修改成功', roles=roles)
    return render_template('assign_user_role.html', roles=roles)


@users.route('/adduser/', methods=['GET', 'POST'])
@is_login
def adduser():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        u_name = User.query.filter_by(username=username).first()
        if u_name:
            return render_template('adduser.html', msg='用户名已存在')
        elif password1 != password2:
            return render_template('adduser.html', msg='两次输入的密码不一致')
        else:
            add = User(username=username, password=password1, role_id=2)
            db.session.add(add)
            db.session.commit()
            return render_template('adduser.html', msg='用户添加成功')
    return render_template('adduser.html')


@users.route('/deluser/')
@is_login
def deluser():
    u_id = request.args.get('u_id')
    User.query.filter_by(u_id=u_id).delete()
    db.session.commit()
    return redirect(url_for('users.userlist'))
