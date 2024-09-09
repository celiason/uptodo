from flask import Flask, render_template, url_for, request, redirect
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# the app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# initialize the db
db = SQLAlchemy(app)

# create a model (i.e. data class ~ row of data)
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    votes = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

# add new tasks (NB: just realized routes need to be above functions)
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding this task!'
    else:
        # ordering todos in db
        # tasks = Todo.query.order_by(Todo.date_created).all()
        tasks = Todo.query.order_by(Todo.votes.desc())
        return render_template('index.html', tasks=tasks)

# delete tasks
@app.route('/delete/<int:id>')
def delete(id:int):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

# edit tasks
@app.route('/edit/<int:id>', methods=["GET","POST"])
def edit(id:int):
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem editing that task'
    else:
        return render_template('edit.html', task=task)

# upvote tasks
@app.route('/upvote/<int:id>')
def upvote(id:int):
    task = Todo.query.get_or_404(id)
    try:
        task.votes = task.votes + 1
        db.session.commit()
        return redirect('/')
    except:
        return redirect('/')

# downvote tasks
@app.route('/downvote/<int:id>')
def downvote(id:int):
    task = Todo.query.get_or_404(id)
    try:
        task.votes = task.votes - 1
        db.session.commit()
        return redirect('/')
    except:
        return redirect('/')

# tag tasks


# run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True, port=8000)
    # changed port because control center using 5000

