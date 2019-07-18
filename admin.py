from flask import Flask, render_template, request,redirect,url_for,flash,session
from flask_login import login_required
from flask import make_response,jsonify
from flask_session.__init__ import Session
from flask_mysqldb import MySQL
# import db_connection as dbconn
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/student_db'
# mysql=dbconn.getConnection()    
# cur=mysql.cursor()
db = SQLAlchemy(app)



class Admin(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(20), unique=False, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)


    def __repr__(self):
        return 'success'

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    class_name=db.Column(db.String(20),nullable=False)
    is_monitor=db.Column(db.Integer,nullable=False)
    studying_subjects=db.Column(db.String(20),nullable=False)

    def __init__(self, class_name,is_monitor,studying_subjects):
      self.class_name=class_name
      self.is_monitor=is_monitor
      self.studying_subjects=studying_subjects

    

class Teacher(db.Model):
    teacher_id = db.Column(db.Integer, primary_key=True)
    department_name=db.Column(db.String(20),nullable=False)
    is_hod=db.Column(db.Integer,nullable=False)
    teaching_subject=db.Column(db.String(20),nullable=False)

    def __init__(self, department_name,is_hod,teaching_subject):
      self.department_name=department_name
      self.is_hod=is_hod
      self.teaching_subject=teaching_subject

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    fname=db.Column(db.String(20),nullable=False)
    lname=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(60),nullable=False)
    mobileno=db.Column(db.String(20),nullable=False)
    about=db.Column(db.String(10),nullable=False)

    def __init__(self, fname,lname,email,mobileno,about):
      self.fname=fname
      self.lname=lname
      self.email=email
      self.mobileno=mobileno
      self.about=about


@app.route('/')
def index():
    return render_template('login.html')  

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == "POST":
        try:
            data = request.get_json()
            uname=data.get('username')
            pass1=data.get('password1')
            registered_admin = Admin.query.filter_by(uname=uname,password=pass1).first()
            if registered_admin is not None:
                response_data={
                    'status_code':200,
                    'message':True,
                    }
                return jsonify(response_data)
            else:
                return jsonify({'result':'Incorrect Username or Password...' }) 
        except:
             response_data={
                    'status_code':501,
                    'result':'Something went wrong....'
                     }
             return jsonify(response_data)

            # cur.execute('SELECT uname,pass FROM admin WHERE uname = %s AND pass = %s', (uname, pass1))
            # idpass = cur.fetchone()

            # if idpass is not None: 

            #     response_data = {
            #         "result": idpass,
            #         "sucess": True,
            #         "status_code": 200,             
            #         }   
            #     return jsonify(response_data)
            # else:
            #     return jsonify({'result':'Incorrect Username or Password...' }) 
            

@app.route('/adminlogout')
def adminlogout():
    return render_template('login.html')

      

@app.route('/userswitch')
def userswitch():
    return render_template('userswitch.html')


@app.route('/admininsert', methods=['POST'])
def admininsert():
    try:
        if request.method == "POST":
            data = request.get_json()
            uname=data.get('username')
            pass1=data.get('password1')
            entry_admin=Admin(uname=uname,password=pass1)
            db.session.add(entry_admin)
            db.session.commit()
            # cur.execute("INSERT INTO admin(uname,pass) VALUES ( %s, %s)", ( uname, pass1))
            # mysql.commit()                    
            return jsonify({'result':'Data added successfully!' })

    except:     
        response_data={
                    'status_code':501,
                    'result':'Something went wrong....'
                     }
        return jsonify(response_data)

@app.route('/register')
def register():
    return render_template('register.html')


# @app.route('/student',methods=['POST'])
# def student():
#     if request.method=='POST':
#         response_data = {
#                 "result": 'Switched to student',
#                 "sucess": True,
#                 "status_code": 200,             
#                 }  
#         return jsonify(response_data)

@app.route('/studentinfo')
def studentinfo():
    # import pdb;pdb.set_trace()
    # cur.execute("SELECT  * FROM stud")
    # data = cur.fetchfirst()
    # return render_template('studentdata.html', stud=data)
    return render_template('studentdata.html', student = Student.query.all() )

@app.route('/studentinsert', methods=['POST'])
def studentinsert():
    
    try:
        if request.method == "POST":
            data = request.get_json()
            class_name=data.get('class_name')
            studying_subjects=data.get('studying_subjects')
            if data.get('is_monitor')=="1":
                is_monitor=1
            else:
                is_monitor=0
            entry_student=Student(class_name=class_name,studying_subjects=studying_subjects,is_monitor=is_monitor)
            db.session.add(entry_student)
            db.session.commit()
            # cur.execute("INSERT INTO stud(class_name,is_monitor,studying_subjects) VALUES (  %s, %s, %s)", (class_name, is_monitor, studying_subjects))
            # mysql.commit()                    
            return jsonify({'result':'Student data added successfully!' })

    except:     
        response_data={
        'status_code':501,
        'result':"Something Went wrong..."
        }
        return jsonify(response_data)

@app.route('/studentdelete/<string:id_data>', methods = ['GET'])
def studentdelete(id_data):
    try:
        # import pdb;pdb.set_trace()
        # cur.execute("DELETE FROM stud WHERE id=%s", (id_data))
        # mysql.commit()
        delete_student=Student.query.filter_by(student_id=id_data).first()
        db.session.delete(delete_student)
        db.session.commit()
        return redirect(url_for('studentinfo'))
    except:     
        response_data={
        'status_code':501,
        'result':"Something Went wrong..."
        }
        return jsonify(response_data)


@app.route('/studentupdate',methods=['POST','GET'])
def studentupdate():
    try:
        if request.method == 'POST':
            data = request.get_json()
            id_data=data.get('id')
            class_name=data.get('class_name')
            studying_subjects=data.get('studying_subjects')
            is_monitor=0
            if data.get('is_monitor')=="1":
                is_monitor=1
            else:
                is_monitor=0
            print(is_monitor)
            update_student=Student.query.filter_by(student_id=id_data).first()
            update_student.class_name=class_name
            update_student.is_monitor=is_monitor
            update_student.studying_subjects=studying_subjects
            db.session.commit()
            # cur.execute("""
            # UPDATE stud
            # SET class_name=%s, is_monitor=%s, studying_subjects=%s  
            # WHERE id=%s""", (class_name, is_monitor,studying_subjects, id_data))
            # mysql.commit()
            return jsonify({'result':'Student data updated successfully!' })

    except:
        return jsonify({'result':'Something went wrong....' })



'''**********Teacher Module***********'''
@app.route('/teacherinfo')
def teacherinfo():
    # import pdb;pdb.set_trace()
    # cur.execute("SELECT  * FROM teacher")
    # data = cur.fetchfirst()
    # return render_template('teacherdata.html', teacher=data)
    return render_template('teacherdata.html', teacher = Teacher.query.all() )

@app.route('/teacherinsert', methods=['POST'])
def teacherinsert():
    
    try:
        if request.method == "POST":
            data = request.get_json()
            department_name=data.get('department_name')
            teaching_subject=data.get('teaching_subject')
            # import pdb; pdb.set_trace()
            if data.get('is_hod')=="0":
                is_hod=0
            else:
                is_hod=1
            # cur.execute("INSERT INTO teacher(department_name,is_hod,teaching_subject) VALUES (  %s, %s, %s)", (department_name, is_hod, teaching_subject))
            # mysql.commit()                    
            entry_teacher=Teacher(department_name=department_name,is_hod=is_hod,teaching_subject=teaching_subject)
            db.session.add(entry_teacher)
            db.session.commit()
            # cur.execute("INSERT INTO student(class_name,is_monitor,studying_subjects) VALUES (  %s, %s, %s)", (class_name, is_monitor, studying_subjects))
            # mysql.commit()                    
            return jsonify({'result':'Teacher data added successfully!' })

    except:     
        response_data={
        'status_code':501,
        'result':'Something went wrong....'
        }
        return jsonify(response_data)

@app.route('/teacherdelete/<string:id_data>', methods = ['GET'])
def teacherdelete(id_data):
    # import pdb;pdb.set_trace()
    # cur.execute("DELETE FROM teacher WHERE id=%s", (id_data))
    # mysql.commit()
    delete_teacher=Teacher.query.filter_by(teacher_id=id_data).first()
    db.session.delete(delete_teacher)
    db.session.commit()
    return redirect(url_for('teacherinfo'))


@app.route('/teacherupdate',methods=['POST','GET'])
def teacherupdate():
    try:
        if request.method == 'POST':
            # import pdb; pdb.set_trace();
            data = request.get_json()
            id_data=data.get('id')
            department_name=data.get('department_name')
            if data.get('is_hod')=="0":
                is_hod=0
            else:
                is_hod=1
            teaching_subject=data.get('teaching_subject')
            # cur.execute("""
            # UPDATE teacher
            # SET department_name=%s, is_hod=%s, teaching_subject=%s  
            # WHERE id=%s""", (department_name, is_hod,teaching_subject, id_data))
            # mysql.commit()
            update_teacher=Teacher.query.filter_by(teacher_id=id_data).first()
            update_teacher.department_name=department_name
            update_teacher.is_hod=is_hod
            update_teacher.teaching_subject=teaching_subject
            db.session.commit()
            return jsonify({'result':'Teacher data updated successfully!' })


    except:
        return jsonify({'result':'Something went wrong!' })
'''*************User Module*********'''
@app.route('/user',methods=['POST'])
def user():
    if request.method=='POST':
        response_data = {
                "result": 'Switched to User',
                "sucess": True,
                "status_code": 200,             
                }  
        return jsonify(response_data)

@app.route('/userinfo')
def userinfo():
        # import pdb;pdb.set_trace()
        # cur.execute("SELECT  * FROM user")
        # data = cur.fetchfirst()
        # return render_template('userdata.html', user=data)
        return render_template('userdata.html', user= User.query.all() )

@app.route('/userinsert', methods=['POST'])
def userinsert():
    try:
        if request.method == "POST":
            
            
            data = request.get_json()
            fname=data.get('first_name')
            lname=data.get('last_name')
            email=data.get('email')
            mobileno1=data.get('phone')
            about=data.get('about')
            registered_user = User.query.filter_by(mobileno=mobileno1).first()
            if registered_user is not None:
                return jsonify({'result':'Mobile number already exist.'}) 
            else:
                entry_user=User(fname=fname,lname=lname,email=email,mobileno=mobileno1,about=about)
                db.session.add(entry_user)
                db.session.commit()
                return jsonify({'result':'User Data added successfully......' })
    except:
            return jsonify({'result':'Something went wrong..........' }) 
            # cur.execute("SELECT mobileno FROM user WHERE mobileno=%s", (mobileno1))
            # row=cur.fetchone()
            # if row is not None:            
            #     return jsonify({'result':'Mobile number already exist.'})
            # else:
            #      cur.execute("INSERT INTO user(fname,lname,email,mobileno,about) VALUES (  %s, %s, %s, %s, %s)", (fname, lname, email, mobileno1, about))
            #      mysql.commit()      

                 

@app.route('/userdelete/<string:id_data>', methods = ['GET'])
def userdelete(id_data):
    # cur.execute("DELETE FROM user WHERE id=%s", (id_data))
    # mysql.commit()
    delete_user=User.query.filter_by(user_id=id_data).first()
    db.session.delete(delete_user)
    db.session.commit()
    return redirect(url_for('userinfo'))


@app.route('/userupdate',methods=['POST','GET'])
def userupdate():
    
    try:
        if request.method == 'POST':
            data = request.get_json()
            id_data=data.get('id')
            fname=data.get('first_name')
            lname=data.get('last_name')
            email=data.get('email')
            mobileno1=data.get('phone')
            about=data.get('about')
            # cur.execute("""
            # UPDATE user
            # SET fname=%s, lname=%s, email=%s, mobileno=%s, about=%s 
            # WHERE id=%s""", (fname, lname, email, mobileno1, about,  id_data))
            # mysql.commit()
            update_user=User.query.filter_by(user_id=id_data).first()
            update_user.fname=fname
            update_user.lname=lname
            update_user.email=email
            update_user.mobileno=mobileno1
            update_user.about=about
            db.session.commit()
            return jsonify({'result':'User data updated successfully!' })

    except:
        return jsonify({'result':'Something went wrong!' })

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

