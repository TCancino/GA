from flask import Flask, flash, render_template, redirect, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
from forms import SignUpForm
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from autohorario import *

import os

import random
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

ramos = []#Guardar RAMOS ingresados
ramos_codes = []#Guardar codigos de RAMOS ya ingresados
ramos_names = []#Guardar nombres de RAMOS ya ingresados
secciones = []#Guardar SECCIONES ingresadas

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
        doc = documento.sheet_by_index(7) #"lee" la primera hoja del Excel
        for i in range(1, doc.nrows): #RECORRER el EXCEL para llenar llenar los arreglos con las clases que corresponden
          if doc.cell_value(i,7) == '': #cambio de sección
            if seccion in secciones:
              pass
            else:
              secciones.append(seccion)
            continue
          else:
            # GUARDAR RAMOS:
            if doc.cell_value(i,1) in ramos_codes: #verificar que el ramo no se haya registrado.
              pass
            else:
              ramos.append(Ramo(doc.cell_value(i,2),doc.cell_value(i,1)))
              ramos_codes.append(doc.cell_value(i,1))
              ramos_names.append(doc.cell_value(i,2))
            # GUARDAR SECCIONES:
            if doc.cell_value(i-1,3) != doc.cell_value(i,3) or doc.cell_value(i-1,1) != doc.cell_value(i,1): #se cumple al cambiar de seccion o ramo
              seccion = Seccion(doc.cell_value(i,3).split(" ")[1], int(doc.cell_value(i,12)), doc.cell_value(i,2))
            aux = doc.cell_value(i,7).split(" ")
            if doc.cell_value(i,5).split(" ")[0] == 'CÁTEDRA' or len(doc.cell_value(i,7)) > 16:
              cat1 = aux[0]
              cat2 = aux[1]
              profe = doc.cell_value(i,9)
              seccion.set_profe(profe)
              if (doc.cell_value(i,2).split(" ")[0] == 'CÁLCULO' and doc.cell_value(i,2).split(" ")[1] != 'III') or doc.cell_value(i,2).split(" ")[0] == 'ÁLGEBRA': #TIENEN 3 CÁTEDRAS
                cat3 = aux[2]
                horario_clases = aux[3]
                seccion.set_clase(cat3, horario_clases)
              else:
                horario_clases = aux[2]
              seccion.set_clase(cat1, horario_clases)
              seccion.set_clase(cat2, horario_clases)
            else:
              dia_clases = aux[0]
              horario_clases = aux[1]
              seccion.set_clase(dia_clases, horario_clases)
        return render_template('choose_classes.html', file = file, r_codes = ramos_codes, r_names = ramos_names, x = len(ramos_codes), sections = secciones)
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

secciones_disp_de_ramos_elegidos = []
@app.route('/options', methods=['GET', 'POST'])
def options():
  if request.method == 'POST':
    nombres_ramos_elegidos = request.form.getlist('my_checkbox')
    #secciones = request.form.getlist('secciones_arr')
    for i in nombres_ramos_elegidos: #Se guardan las secciones disponibles de cada ramo en un arreglo respectivo.
      secciones_del_ramo_i = []
      for j in secciones:
        if i == j.get_ramo_nom(): #si el nombre del ramo de la seccion es igual al nombre del ramo que se desea tomar se cumple la condicion
          secciones_del_ramo_i.append(j) #guarda en el arreglo un arreglo con las secciones que hay del ramo 'i'
      secciones_disp_de_ramos_elegidos.append(secciones_del_ramo_i)
    return render_template('options.html')
  return render_template('signup.html')

combi_secciones = []
Horarios = []
horarios_totales = 0
@app.route('/horario', methods=['GET','POST'])
def horario():
  if request.method == 'POST':
    cant_ramos = len(secciones_disp_de_ramos_elegidos)
    opcion_elegida = int(request.form.get('my_checkbox'))
    show_horario = int(request.form.get('aux'))
    combi_secciones = combinacion_de_secciones_1(cant_ramos, secciones_disp_de_ramos_elegidos, opcion_elegida)
    horarios_totales = len(combi_secciones)
    if cant_ramos == 0:
      return 'No Hay Combinaciones Posibles'
    for c_s in combi_secciones:
      Horarios.append(hacer_horario(c_s))
    Horario = Horarios[show_horario]
    return render_template('horario.html', show_horario = show_horario, horarios_totales = horarios_totales, Horario = Horario)
  else:
    return render_template('index.html')

@app.route('/otros_horarios', methods=['GET','POST'])
def otros_horarios():
  if request.method == 'POST':
    show_horario = int(request.form.get('aux')) + 1
    horarios_totales = len(Horarios)
    if show_horario == horarios_totales:
      return 'Show_horario = '+ str(show_horario) + '\n Horarios_totales = ' + str(horarios_totales)
    Horario = Horarios[show_horario]
    return render_template('horario.html', show_horario = show_horario, horarios_totales = horarios_totales, Horario = Horario)
  return 'Method GET'

@app.route('/chosen_one', methods=['GET','POST'])
def chosen_one():
  if request.method == 'POST':
    show_horario = int(request.form.get('aux'))
    Horario = Horarios[show_horario]
    return render_template('chosen_one.html', show_horario = show_horario, Horario = Horario)

if __name__== '__main__':
  db.create_all()
  Bootstrap(app)
  app.run('0.0.0.0', 5000, debug=True)