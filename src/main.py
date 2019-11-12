from base import *
from functions import *
app = create_app()

@app.route('/',methods = ['GET','POST'])
def loginPage():
    
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['psw']
        loginType = request.form['type']

        if loginType == 'Student':
            user,student = loginStudent(username,password)

        elif loginType == 'Teacher':
            user,teacher = loginTeacher(username,password)

        elif loginType == 'Admin':
            user = loginAdmin(username,password)

        if user == None:
            print(f"No Such {loginType}")
            return redirect(url_for('loginPage'))
        else:
            print(user.uuid)

    if request.method == 'GET':
        uuid = request.cookies.get('uuid')
        return render_template('lp1.html')

@app.route('/student')
def studentPage():

    return getStudents('D',3)[0].name

@app.route('/admin',methods = ['GET','POST'])
def adminPage():

    if request.method == 'POST':

        if request.form['submit_button'] == "Add Teacher":
            print(request.form)

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

if __name__ == '__main__':
    app.run(debug = True)