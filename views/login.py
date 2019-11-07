from flask import Blueprint,render_template,request,session,redirect,url_for
from models.models import *
from utils.ch_login import *

logins = Blueprint('logins',__name__)
@logins.route('/login/',methods=['GET','POST'])
# @is_login
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        Login = User.query.filter_by(username=username,password=password).first()
        if Login:
            session['user_id'] = Login.u_id
            session['username'] = Login.username
            return render_template('index.html')
        else:
            msg='* 用户名密码不一致'
            return render_template('login.html',msg=msg)
    return render_template('login.html')

@logins.route('/head/')
@is_login
def head():
    user = session.get('username')
    return render_template('head.html',user=user)

@logins.route('/left/')
@is_login
def left():
    user = session.get('username')
    permissions = User.query.filter_by(username=user).first().role.permission
    return render_template('left.html',permissions=permissions)

@logins.route('/register/',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        pwd1 = request.form.get('pwd1')
        pwd2 = request.form.get('pwd2')
        password = (pwd1 == pwd2)
        user = User.query.filter_by(username=username).first()
        if password and not user:
            reg = User(username=username,password=pwd1,role_id=2)
            db.session.add(reg)
            db.session.commit()
            return redirect(url_for('logins.login'))
        elif user:
            return render_template('register.html',msg='用户名已存在')
        else:
            return render_template('register.html',msg='两次输入的密码不一致')

    return render_template('register.html')

@logins.route('/grade/')
@is_login
def gradelist():
    page = int(request.args.get('page',1))
    paginate = Grade.query.paginate(page,2,False)
    grades = paginate.items
    return render_template('grade.html',paginate=paginate,grades=grades)

@logins.route('/logout/',methods=['GET','POST'])
@is_login
def logout():
    session.clear()
    return redirect(url_for('logins.login'))


@logins.route('/changepwd/',methods=['GET','POST'])
@is_login
def changepwd():
    user = User.query.filter_by(u_id=session.get('user_id')).first()
    password = user.password
    if request.method == 'POST':
        pwd = request.form.get('pwd1')
        newpwd1 = request.form.get('pwd2')
        newpwd2 = request.form.get('pwd3')
        if pwd != password:
            return render_template('changepwd.html',user=user,msg='旧密码输入错误')
        elif newpwd1 != newpwd2:
            return render_template('changepwd.html',user=user,msg='两次输入的密码不一致')
        else:
            user.password = newpwd1
            db.session.commit()
            return render_template('changepwd.html',user=user,msg='密码修改成功')
    return render_template('changepwd.html',user=user)