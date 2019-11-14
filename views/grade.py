from flask import Blueprint, render_template, request, session, redirect, url_for
from models.models import *
from utils.ch_login import *

grades = Blueprint('grades', __name__)


@grades.route('/grade_student/', methods=['GET', 'POST'])
@is_login
def grade_student():
    # print(session.get('username'))
    g_id = int(request.args.get('g_id', 1))
    stus = Student.query.filter_by(grade_id=g_id).all()
    paginate = Student.query.filter_by(s_id=g_id).paginate(1, 50, False)
    return render_template('student.html', stus=stus, paginate=paginate)


@grades.route('/edit_grade/', methods=['GET', 'POST'])
@is_login
def edit_grade():
    g_id = request.args.get('g_id')
    g_name = Grade.query.filter_by(g_id=g_id).first().g_name
    if request.method == 'POST':
        g_id = request.args.get('g_id')
        Grade.query.filter_by(g_id=g_id).first().g_name = request.form.get('g_name')
        db.session.commit()
        return redirect(url_for('logins.gradelist'))
    else:
        return render_template('addgrade.html', g_name=g_name)


@grades.route('/addgrade/', methods=['GET', 'POST'])
@is_login
def addgrade():
    if request.method == 'POST':
        g_name = request.form.get('g_name')
        exits = Grade.query.filter_by(g_name=g_name).first()
        if exits:
            return render_template('addgrade.html', msg='班级已存在')
        elif g_name == '':
            return render_template('addgrade.html', msg='班级名称不得为空')
        else:
            add = Grade(g_name=g_name)
            db.session.add(add)
            db.session.commit()
            return render_template('addgrade.html', msg='班级添加成功')
    else:
        return render_template('addgrade.html')


@grades.route('/del_grade/')
@is_login
def del_grade():
    g_id = request.args.get('g_id')
    Student.query.filter_by(grade_id=g_id).delete()
    Grade.query.filter_by(g_id=g_id).delete()
    db.session.commit()
    return redirect(url_for('logins.gradelist'))
