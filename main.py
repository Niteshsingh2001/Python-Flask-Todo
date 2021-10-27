from flask import Flask, render_template , url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
db= SQLAlchemy(app)

class todo(db.Model):

    id = db.Column(db.Integer, primary_key=True)    
    text = db.Column(db.String(200), nullable=False)    
    completed = db.Column(db.Integer, default= 0)   
    date_cre =  db.Column(db.DateTime, default = datetime.utcnow)  

    def __repr__(Self):
        # return "<task %r>"% Self.id
        return "f<task {self.id}>"

@app.route("/", methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        task_cont = request.form['content']
        new_task = todo(text= task_cont)

        try:
            db.session().add(new_task)
            db.session.commit()
            return redirect('/')

        except:
            return "there is an issue"
    else:
        tasks= todo.query.order_by(todo.date_cre).all()
        return render_template("index.html", tasks=tasks)

    
@app.route("/delete/<int:id>", methods = ['POST','GET'])
def delete(id):
    del_task = todo.query.get_or_404(id)
    try:
        db.session.delete(del_task)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return "error ",e   

@app.route("/update/<int:id>", methods = ['POST','GET'])
def update(id): 
      up = todo.query.get_or_404(id)
      if request.method == 'POST':
          
          up.text = request.form['content']
          try:
              db.session.commit()
              return redirect('/')
          except:
                return "there is an issue"
      else:
          return render_template("update.html" ,tas=up)


if __name__ == "__main__":
    app.run(debug = True)
