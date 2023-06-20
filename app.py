from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# For database, using sqlite
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
db=SQLAlchemy(app)

# creating our database using class(defining the schema)
class Todo(db.Model):
    sno=db.Column(db.Integer, primary_key=True)

    title=db.Column(db.String(50), nullable=False)

    desc=db.Column(db.String(100), nullable=False)

    date_created=db.Column(db.DateTime, default=datetime.utcnow)

    # Jab bhi todo ka koi object print karoge to kya dekhna chahte ho, title and sno
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    
with app.app_context():
    db.create_all()

@app.route("/", methods=['GET', 'POST'])
def home():

    if request.method=='POST':
        # print("post")
        # print(request.form['title'])
        title=request.form['title']
        desc=request.form['desc']

        # whenever someone submits the form, the todo is added in db
        todo=Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    allTodo=Todo.query.all()
    # index.html will be rendered
    return render_template('index.html', allTodo=allTodo)
    # return "<p>Hello, World!</p>"

@app.route("/show")
def products():
    allTodo=Todo.query.all()
    print(allTodo)
    return "<p>This is show page</p>"

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        db.session.add(todo)
        todo.title=title
        todo.desc=desc
        db.session.commit()
        return redirect('/')
    
    allTodo=Todo.query.filter_by(sno=sno)
    return render_template('update.html', allTodo=allTodo)
    

@app.route('/delete/<int:sno>')
def delete(sno):
    allTodo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(allTodo)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
    