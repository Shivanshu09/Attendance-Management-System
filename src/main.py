from base import *
from functions import *
app = create_app()

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id = user_id).first()

def reroute(loginType):

    if loginType == 'Student':
        return redirect(url_for('studentPage'))
        
    elif loginType == 'Teacher':
        return redirect(url_for('teacherPage'))
        
    elif loginType == 'Admin':
        return redirect(url_for('adminPage'))

@app.route('/',methods = ['GET','POST'])
def loginPage():
    
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['psw']
        loginType = request.form['type']

        if loginType == 'Student':
            user = loginStudent(username,password)

        elif loginType == 'Teacher':
            user = loginTeacher(username,password)

        elif loginType == 'Admin':
            user = loginAdmin(username,password)

        print(user)

        if user == None:
            return redirect(url_for('loginPage'))

        
        login_user(user)
        return reroute(loginType)

    if request.method == 'GET':
        
        # if current_user.is_anonymous == True:
        return render_template('lp1.html')

@app.route('/teacher')
@login_required(role = 'Teacher')
def teacherPage():

    teacher = Teachers.query.filter_by(id = current_user.get_id()).first()
    subject = Subject.query.filter_by(id = teacher.subject).first().name
    return render_template('teacher.html',classes = teacher.classes,name = teacher.name,subject = subject)

@app.route('/logout')
@login_required(role = 'ANY')
def logout():
    logout_user()
    return redirect(url_for('loginPage'))

@app.route('/student')
@login_required(role = 'Student')
def studentPage():

    return render_template('student.html')

@app.route('/admin',methods = ['GET','POST'])
@login_required(role = 'Admin')
def adminPage():

    if request.method == 'POST':

        if request.form['submit_button'] == "Add Teacher":
            createTeacher(request.form)

        elif request.form['submit_button'] == "Add Student":
            
            usrname = int(request.form['st_id'])
            name = request.form['st_name']
            psswrd = request.form['st_password']
            sec = request.form['st_section']
            sem = request.form['st_sem']
            email = request.form['st_email']
            
            createStudent(name,usrname,psswrd,sec,sem)

        elif request.form['submit_button'] == "Add Class":
            
            sec = request.form['tc_section']
            sem = request.form['tc_semester']
            createClass(sec, sem)

    return render_template('admin.html')

@app.route('/getStudents',methods = ['POST'])
@login_required(role = 'Teacher')
def studentList():

    if request.method == 'POST':
        sem = request.json['semester']
        sec = request.json['section']
        
    return jsonify(getStudents(sec,sem))



if __name__ == '__main__':
    app.run(debug = True)