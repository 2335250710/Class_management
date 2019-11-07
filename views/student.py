from flask import Blueprint,render_template,url_for,redirect,request
from models.models import *
from utils.ch_login import *

students = Blueprint('students',__name__)


@students.route('/student/')
@is_login
def student():
    page = int(request.args.get('page',1))
    paginate = Student.query.paginate(page,3,False)
    stus = paginate.items
    return render_template('student.html',stus=stus,paginate=paginate)


@students.route('/addstu/',methods=['GET','POST'])
@is_login
def addstu():
    grades = Grade.query.all()
    if request.method == 'POST':
        s_sex = int(request.form.get('s_sex'))
        g_name = request.form.get('g_name')
        s_name = request.form.get('s_name')
        if s_name == '':
            msg = '学生姓名不能为空'
            return render_template('addstu.html', msg=msg)
        elif g_name is None:
            msg = '请选择班级'
            return render_template('addstu.html',msg=msg)
        else:
            grade_id = Grade.query.filter_by(g_id=g_name).first().g_id
            add = Student(s_sex=s_sex,s_name=s_name,grade_id=grade_id)
            db.session.add(add)
            db.session.commit()
            msg = '添加成功'
            return render_template('addstu.html',msg=msg,grades=grades)
    else:
        return render_template('addstu.html',grades=grades)


@students.route('/student/delete/')
@is_login
def delete():
    s_id = int(request.args.get('s_id'))
    Student.query.filter_by(s_id=s_id).delete()
    db.session.commit()
    return redirect(url_for('students.student'))