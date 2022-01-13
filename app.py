from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import urllib

HOSTNAME = os.uname().nodename # Does not work on Windows.
CERTS_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/certs'
MYSQL_URI = os.environ.get('MYSQL_URI', None)
CACERT_URL = os.environ.get('CACERT_URL', None)
CACERT_FILE = os.environ.get('CACERT_FILE', None)

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # to supress cli grizzling
if MYSQL_URI:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + MYSQL_URI
    if CACERT_URL: # FIXME: cannot report bad cert url to user, app will die.
        cacert_filename = os.path.join(CERTS_FOLDER, os.path.basename(urllib.parse.urlparse(CACERT_URL).path))
        urllib.request.urlretrieve(CACERT_URL, cacert_filename)
        app.config['SQLALCHEMY_DATABASE_URI'] += '?ssl_ca=' + cacert_filename
    elif CACERT_FILE:
        cacert_filename = os.path.join(CERTS_FOLDER, CACERT_FILE)
        app.config['SQLALCHEMY_DATABASE_URI'] += '?ssl_ca=' + cacert_filename

else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}>'

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
            return render_template('error.html', error='Nem sikerült a feladat felvétele.')
    else:
        try:
            tasks = Todo.query.order_by(Todo.date_created).all()
        except:
            return render_template('error.html', error=f'Nem sikerült kapcsolódni az adatbázishoz ({app.config["SQLALCHEMY_DATABASE_URI"]}).')
        return render_template('index.html', tasks=tasks, message=f'kiszolgáló: {HOSTNAME}')

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return render_template('error.html', error='Nem sikerült a feladat törlése.')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task_to_update.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return render_template('error.html', error='Nem sikerült a feladat frissítése.')
    else:        
        return render_template('update.html', task=task_to_update, message=f'kiszolgáló: {HOSTNAME}')


if __name__ == '__main__':
    app.run(debug = True)