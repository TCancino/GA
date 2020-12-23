from flask import Flask, flash, render_template, redirect, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
from forms import SignUpForm
from flask_sqlalchemy import SQLAlchemy

import os

import xlrd #para leer planillas Excel

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
  new_post = Posts( username='username', password=1234)
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
      archivo , ext = os.path.splitext(file.filename)
      if ext == '.xlsx' or ext == '.xlsm' or ext == '.xlsb' or ext == '.xml' or ext == '.xltx' or ext == '.xlt' or ext == '.xls' or ext == '.xla':
        file.save(os.path.join(app.config["EXCEL_UPLOADS"], file.filename))
        documento = xlrd.open_workbook("./static/files/"+file.filename) #'abre' el Excel
        doc = documento.sheet_by_index(0) #"lee" la primera hoja del Excel
        nombres_ramos = []
        codigos_ramos = []
        x = 0
        for i in range(1, doc.nrows):
          if doc.cell_value(i,1) in codigos_ramos: #verificar que el ramo no se haya registrado.
            pass
          else:
              nombres_ramos.append(doc.cell_value(i,2))
              codigos_ramos.append(doc.cell_value(i,1))
              x = x + 1
        return render_template('choose_classes.html', file = file, r_codes = codigos_ramos, r_names = nombres_ramos, x = x)
      else:
        flash('Tipo de Archivo Incorrecto.')
        return render_template('signup.html')
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

@app.route('/choose_classes', methods=['GET', 'POST'])
def choose_classes():
  if request.method == 'GET':
    return render_template('choose_classes.html')
  else:
    return render_template('choose_classes.html')

if __name__== '__main__':
  db.create_all()
  app.run('0.0.0.0', 5000, debug=True)