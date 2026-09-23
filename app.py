from flask import Flask, request, jsonify,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///student.db"

db=SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    course = db.Column(db.String(100),nullable=False)
    stream=db.Column(db.String(100),nullable=False)
with app.app_context():
    db.create_all()

@app.route("/",methods=["POST","GET"])
def login():
     if request.method == "POST":
      username=request.form.get("username")
      password = request.form.get("password")
      if username == "yash" and password == "yash@123":
            return render_template("student.html")
     return render_template("/login.html")



@app.route("/student")
def student():
        students=db.session.execute(
             db.select(Student)
        ).scalars().all() 
        return render_template("student.html",students=students)

@app.route("/add_student",methods=["POST","GET"])
def add():
     if request.method == "POST":
          name=request.form.get("name")
          age = request.form.get("age")
          course = request.form.get("course")
          stream= request.form.get("stream")

          student =Student(name=name,age=age,course=course,stream=stream)

          db.session.add(student)
          db.session.commit()
          return render_template("student.html")
     return render_template("add_student.html")

@app.route("/edit_student/<int:id>",methods=["POST","GET"])
def edit_student(id):
     student=Student.query.get_or_404(id)
     if request.method == "POST":
       name = request.form.get("name")
       age = request.form.get("age")
       course = request.form.get("course")
       stream= request.form.get("stream")
       student.age=age
       student.name=name
       student.course=course
       student.stream=stream
       db.session.commit()
       return redirect(url_for("student"))
     else:
          return render_template("edit_student.html",
                                 id=student.id,
                                 name=student.name,
                                 age=student.age,
                                 course=student.course,
                                 stream=student.stream)

@app.route("/delete_student/<int:id>",methods=["POST"])
def delete(id):
     student=Student.query.get_or_404(id)
     db.session.delete(student)
     db.session.commit()
     return redirect(url_for("student"))
if __name__ == "__main__":
    app.run(debug=True)
