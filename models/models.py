from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

#班级模型类
class Grade(db.Model):
    g_id = db.Column(db.Integer,primary_key=True)
    g_name = db.Column(db.String(20),unique=True)
    g_create_time = db.Column(db.DateTime,default=datetime.now)
    students = db.relationship('Student',backref='grade')

    __tablename__ = 'grade'


#学生模型类
class Student(db.Model):
    s_id = db.Column(db.Integer,primary_key=True)
    s_name = db.Column(db.String(16))
    s_sex = db.Column(db.Integer)
    grade_id = db.Column(db.Integer,db.ForeignKey('grade.g_id'),nullable=True)

    __tablename__ = 'student'


#用户模型类
class User(db.Model):
    u_id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(16),unique=True)
    password = db.Column(db.String(250))
    u_create_time = db.Column(db.DateTime,default=datetime.now)
    role_id = db.Column(db.Integer,db.ForeignKey('role.r_id'))

    __tablename__ = 'user'


#角色模型类
class Role(db.Model):
    r_id = db.Column(db.Integer,primary_key=True)
    r_name = db.Column(db.String(10))
    users = db.relationship('User',backref='role')

    __tablename__ = 'role'


#角色权限关联表
r_p = db.Table('r_p',
               db.Column('role_id',db.Integer,db.ForeignKey('role.r_id'),primary_key=True),
               db.Column('permission_id',db.Integer,db.ForeignKey('permission.p_id'),primary_key=True))


#权限模型表
class Permission(db.Model):
    p_id = db.Column(db.Integer,primary_key=True)
    p_name = db.Column(db.String(16),unique=True)
    p_er = db.Column(db.String(16),unique=True)
    roles = db.relationship('Role',secondary=r_p,backref=db.backref('permission',lazy=True))

    __tablename__ = 'permission'