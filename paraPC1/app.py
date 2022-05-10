# imports
import sys
from flask import (
    Flask,
    abort,
    jsonify,
    render_template,
    request,
    redirect,
    url_for
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import date

# configurations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/practica'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# models
class User(db.Model):
    __tablename__ = 'usuario'
    username = db.Column(db.String(), primary_key=True)
    password = db.Column(db.String(), nullable=False)
    fecha = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'Usuario: {self.username}'

# db.create_all()

# controllers
@app.route('/')
def index():
    return render_template('index.html', users=User.query.all())

@app.route('/create', methods=['POST', 'GET'])
def create():
    error = False
    response = {}
    try:
        """
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        """
        username = request.get_json()['username']
        password = request.get_json()['password']
        response['username'] = username
        response['password'] = password

        usuario = User(username=username, password=password, fecha=date.today())
        db.session.add(usuario)
        db.session.commit()
    except Exception as e:
        error = True
        print(e)
        print(sys.exs_info())
        db.session.rollback()
    finally:
        db.session.close()
    """
    return redirect(url_for('index'))
    """
    if error:
        abort(500)
    else:
        return jsonify(response)

# run
if __name__ == '__main__':
    app.run(debug=True, port=5000)