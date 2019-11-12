from base import db, User, Teachers, Students, Class
from functools import wraps
from flask_login import current_user
from base import login_manager

def login_required(role = 'ANY'):

    def wrapper(fn):

        @wraps(fn)

        def decorated_view(*args,**kwargs):

            if current_user.get_id() == None:
                return login_manager.unauthorized()

            if current_user.getRole() != role and role != 'ANY':
                return login_manager.unauthorized()
            
            return fn(*args,**kwargs)
        
        return decorated_view
    return wrapper


def loginStudent(usrname,pswrd):
    
    user = User.query.filter_by(id = usrname, pwd = pswrd, role = 'Student').first()

    if user != None:
        student = Students.query.filter_by(id = user.id).first() 
        return user,student

    return None,None

def loginTeacher(usrname,pswrd):
    
    user = User.query.filter_by(id = usrname, pwd = pswrd, role = 'Teacher').first()

    if user != None:
        teacher = Teachers.query.filter_by(id = user.id).first() 
        return user,teacher

    return None,None

def loginAdmin(usrname,pswrd):

    user = User.query.filter_by(id = usrname, pwd = pswrd, role = 'Admin').first()
    return user

def createTeacher(name,username,passkey,classes = ''):
    
    newTeacher = Teachers(name = name,id = username,classes = classes)
    db.session.add(newTeacher)
    db.session.commit()

def createStudent(name,usrname,passkey,sec,sem):
    
    newUser = User(id = usrname, pwd = passkey,role = 'Student',authenticated = False)
    clssroom = Class.query.filter_by(section = sec, semester = sem).first()
    newStudent = Students(name = name,id = usrname, classroom = clssroom)
    db.session.add(newUser)
    db.session.add(newStudent)
    db.session.commit()

def createClass(sec, sem):

    newClass = Class(section = sec,semester = sem)
    db.session.add(newClass)
    db.session.commit()

def getStudents(sec, sem):
    clssroom = Class.query.filter_by(section = sec, semester = sem).first()
    return clssroom.classStudents