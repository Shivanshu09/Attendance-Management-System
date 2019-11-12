from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user
import datetime

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():

    app = Flask(__name__,template_folder='../frontend/html/',static_folder='../frontend/static/css/')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/test.db'
    app.config['SECRET_KEY'] = '91914023582d45d3ad243d43abaf7e8f'
    db.init_app(app)
    
    login_manager.init_app(app)
    
    with app.app_context():

        db.create_all()
    
    return app

class User(db.Model):

    __tablename__ = 'User'

    id = db.Column(db.Integer,primary_key=True)
    pwd = db.Column(db.String())
    role = db.Column(db.String())

    def is_active(self):
        return True

    def getRole(self):
        return self.role

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True
    
    def is_anonymous(self):
        return False

class Class(db.Model):

    __tablename__ = 'Class'

    id = db.Column(db.Integer,primary_key = True)
    section = db.Column(db.String,nullable = False)
    semester = db.Column(db.String, nullable = False)
    subjects = db.relationship('Subject', secondary = 'subject_Class_Relationship')

class Teachers(db.Model):

    __tablename__ = 'Teachers'

    id = db.Column(db.Integer,primary_key = True)
    classes = db.relationship('Class', secondary = 'teacher_Class_Relationship')
    subject = db.Column(db.Integer,db.ForeignKey('Subjects.id'))
    name = db.Column(db.String, nullable = False)

class Students(db.Model):

    __tablename__ = 'Students'
    id = db.Column(db.Integer,primary_key = True)
    classroom_id = db.Column(db.Integer, db.ForeignKey('Class.id', ondelete = 'CASCADE'))
    classroom = db.relationship('Class',backref = db.backref('classStudents',lazy = True))
    name = db.Column(db.String, nullable = False)

class teacherClassRelationship(db.Model):

    __tablename__ = 'teacher_Class_Relationship'

    id = db.Column(db.Integer,primary_key = True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('Teachers.id',ondelete = 'CASCADE'))
    class_id = db.Column(db.Integer, db.ForeignKey('Class.id',ondelete = 'CASCADE'))

class Subject(db.Model):

    __tablename__ = 'Subjects'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String,nullable = False)

class Attendance(db.Model):

    __tablename__ = 'attendance_record'

    id = db.Column(db.Integer,primary_key = True)
    student = db.Column(db.Integer, db.ForeignKey('Students.id',ondelete = 'CASCADE'))
    subject = db.Column(db.Integer, db.ForeignKey('Subjects.id',ondelete = 'CASCADE'))
    date = db.Column(db.Date, nullable = False)
    present = db.Column(db.Boolean,default = False)

class subjectClassRelationship(db.Model):

    __tablename__ = 'subject_Class_Relationship'

    id = db.Column(db.Integer,primary_key = True)
    subject_id = db.Column(db.Integer, db.ForeignKey('Subjects.id',ondelete = 'CASCADE'))
    class_id = db.Column(db.Integer, db.ForeignKey('Class.id',ondelete = 'CASCADE'))