# Imports
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

# Configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/dbp10'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return 'Person: id={}, name={}'.format(self.id, self.name)

db.create_all()

# Controllers
@app.route('/')
def index():
    persons = Person.query.all()
    return 'Hello all: {}'.format(", ".join([p.name for p in persons]))

@app.route('/greetings')
def greetings():
    name = request.args.get('name', '') # caso no exista, se pasa vacio: ''
    lastname = request.args.get('lastname', '')
    # return 'Hola <strong>{}</strong> <script>alert("{}");</script>'.format(name, lastname)
    greetings_str = 'Hola {} {}'.format(name, lastname)
    return render_template('index.html', data=greetings_str)


"""
Desde el cliente se pueden hacer cambios a la pagina web:
127.0.0.1:5001/greetings?name=<strong>Pedro</strong>&lastname=<script>alert(Fernandez);</script>
Estamos escribiendo JS como usuario -> Vulnerabilidad de la pagina web (Cros-Site Scripting XXS)
"""

# Runner
if __name__ == '__main__':
    app.run(debug=True, port=5001) # default port is 5000