from base import db, User, Teachers, Students, Class

def loginStudent(usrname,pswrd):
    
    user = User.query.filter_by(username = usrname, pwd = pswrd, authenticated = True).first()

    if user != None:
        student = Students.query.filter_by(id = user.id).first() 
        return user,student

    return None,None

def loginTeacher(usrname,pswrd):
    
    user = User.query.filter_by(username = usrname, pwd = pswrd).first()

    if user != None:
        teacher = Teachers.query.filter_by(id = user.id).first() 
        return user,teacher

    return None,None

def loginAdmin(usrname,pswrd):

    user = User.query.filter_by(username = usrname, pwd = pswrd).first()
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