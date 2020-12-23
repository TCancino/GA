from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
from forms import SignUpForm
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

import os

dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'thecodex'

class Posts(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(50))
  password = db.Column(db.String(50))
  #username = db.Column(db.String(50), unique=True, nullable=False)

@app.route("/insert/default")
def insert_default():
  new_post = Posts( username='thomas', password=1234)
  db.session.add(new_post)
  db.session.commit()

  return "the default post was create."

class UploadForm(FlaskForm):
  file = FileField()

app.config["EXCEL_UPLOADS"] = "./static/files"

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'POST':
    if request.files:
      new_post = Posts(username=request.form["username"], password=request.form["password"])
      db.session.add(new_post)
      db.session.commit()
      file = request.files['excel']
      file.save(os.path.join(app.config["EXCEL_UPLOADS"], file.filename))
      return redirect(request.url)
  return render_template('signup.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
  form = UploadForm()

  if form.validate_on_submit():
      filename = secure_filename(form.file.data.filename)
      form.file.data.save('uploads/' + filename)
      return redirect(url_for('upload'))

  return render_template('upload.html', form=form)

@app.route('/')
def hello_world():
  return render_template('index.html')

if __name__== '__main__':
  db.create_all()
  Bootstrap(app)
  app.run('0.0.0.0', 5000, debug=True)