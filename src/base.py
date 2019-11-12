from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():

    app = Flask(__name__,template_folder='../frontend/html/',static_folder='../frontend/static/css/')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/test.db'
    
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
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        return True

    def get_id(self):
        return self.username

    def is_authenticated(self):
        return self.authenticated
    
    def is_anonymous(self):
        return False

class Class(db.Model):

    __tablename__ = 'Class'

    id = db.Column(db.Integer,primary_key = True)
    section = db.Column(db.String,nullable = False)
    semester = db.Column(db.String, nullable = False)

class Teachers(db.Model):

    __tablename__ = 'Teachers'

    id = db.Column(db.Integer,primary_key = True)
    classes = db.relationship('Class', secondary = 'teacher_Class_Relationship')
    name = db.Column(db.String, nullable = False)

class Students(db.Model):

    __tablename__ = 'Students'
    id = db.Column(db.Integer,primary_key = True)
    classroom_id = db.Column(db.Integer, db.ForeignKey('Class.id'))
    classroom = db.relationship('Class',backref = db.backref('classStudents',lazy = True))
    name = db.Column(db.String, nullable = False)

class teacherClassRelationship(db.Model):

    __tablename__ = 'teacher_Class_Relationship'

    id = db.Column(db.Integer,primary_key = True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('Teachers.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('Class.id'))