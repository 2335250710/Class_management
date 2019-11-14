from flask import Blueprint, render_template, redirect, url_for, request
from models.models import *
from utils.ch_login import *

permissions = Blueprint('permissions', __name__)


@permissions.route('/roles/', methods=['GET', 'POST'])
@is_login
def roles():
    roles = Role.query.all()
    return render_template('roles.html', roles=roles)


@permissions.route('/userperlist/', methods=['GET', 'POST'])
@is_login
def userperlist():
    r_id = request.args.get('r_id')
    permissions = Role.query.filter_by(r_id=r_id).first().permission
    return render_template('permissions.html', permissions=permissions)


@permissions.route('/eidtorpermission/', methods=['GET', 'POST'])
@is_login
def eidtorpermission():
    p_id = request.args.get('p_id')
    pers = Permission.query.filter_by(p_id=p_id).first()
    if request.method == 'POST':
        p_id = request.args.get('p_id')
        p_name = request.form.get('p_name')
        p_er = request.form.get('p_er')
        pers = Permission.query.filter_by(p_id=p_id).first()
        if p_name == '':
            return render_template('addpermission.html', msg='权限名称不能为空', pers=pers)
        elif p_er == '':
            return render_template('addpermission.html', msg1='简写不能为空', pers=pers)
        else:
            pers.p_name = p_name
            pers.p_er = p_er
            db.session.commit()
            msg = '编辑成功'
            return render_template('addpermission.html', msg=msg, pers=pers)
    else:
        return render_template('addpermission.html', pers=pers)


@permissions.route('/adduserper/', methods=['GET', 'POST'])
@is_login
def adduserper():
    r_id = request.args.get('r_id')
    pers = Permission.query.all()
    if request.method == 'POST':
        p_id = request.form.get('p_id')
        p_name = Permission.query.filter_by(p_id=p_id).first().p_name
        permissions = Role.query.filter_by(r_id=r_id).first().permission
        pname = [i.p_name for i in permissions]
        if p_name in pname:
            return render_template('add_user_per.html', msg='已有该权限', pers=pers)
        else:
            role = Role.query.get(r_id)
            permission = Permission.query.get(p_id)
            permission.roles.append(role)
            db.session.add(permission)
            db.session.commit()
            return render_template('add_user_per.html', msg='权限添加成功', pers=pers)
    return render_template('add_user_per.html', pers=pers)


@permissions.route('/subuserper/', methods=['GET', 'POST'])
@is_login
def subuserper():
    r_id = request.args.get('r_id')
    pers = Role.query.filter_by(r_id=r_id).first().permission
    if request.method == 'POST':
        p_id = request.form.get('p_id')
        role = Role.query.get(r_id)
        permission = Permission.query.get(p_id)
        permission.roles.remove(role)
        db.session.commit()
        pers = Role.query.filter_by(r_id=r_id).first().permission
        return render_template('add_user_per.html', pers=pers, msg='移除成功')
    return render_template('add_user_per.html', pers=pers)


@permissions.route('/addroles/', methods=['GET', 'POST'])
@is_login
def addroles():
    if request.method == 'POST':
        r_name = request.form.get('r_name')
        if r_name == '':
            return render_template('addroles.html', msg='角色名称不能为空')
        else:
            # Role.query.filter_by(r_name=r_name).delete()
            add = Role(r_name=r_name)
            db.session.add(add)
            db.session.commit()
            return render_template('addroles.html', msg='添加成功')
    return render_template('addroles.html')


@permissions.route('/permissions/', methods=['GET', 'POST'])
@is_login
def permission():
    permissions = Permission.query.all()
    return render_template('permissions.html', permissions=permissions)


@permissions.route('/addpermission/', methods=['GET', 'POST'])
@is_login
def addpermission():
    if request.method == 'POST':
        p_name = request.form.get('p_name')
        p_er = request.form.get('p_er')
        if p_name == '':
            return render_template('addpermission.html', msg='权限名称不能为空', pers=None)
        elif p_er == '':
            return render_template('addpermission.html', msg1='简写不能为空', pers=None)
        else:
            per = Permission(p_name=p_name, p_er=p_er)
            db.session.add(per)
            db.session.commit()
            return render_template('addpermission.html', msg1='权限添加成功', pers=None)
    return render_template('addpermission.html', pers=None)


@permissions.route('/delpermission/')
@is_login
def delpermission():
    p_id = request.args.get('p_id')
    permission = Permission.query.get(p_id)
    role = Role.query.all()
    for i in role:
        if permission in i.permission:
            permission.roles.remove(i)
    Permission.query.filter_by(p_id=p_id).delete()
    db.session.commit()
    return redirect(url_for('permissions.permission'))
