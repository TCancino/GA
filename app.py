from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
from forms import SignUpForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'thecodex'

class UploadForm(FlaskForm):
  file = FileField()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignUpForm()
  if form.is_submitted():
    result = request.form
    return render_template('user.html', result=result)
  return render_template('signup.html', form=form)

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
  app.run('0.0.0.0', 5000, debug=True)