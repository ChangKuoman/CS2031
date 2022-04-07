# Imports
from flask import Flask
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

# Runner
if __name__ == '__main__':
    app.run(debug=True, port=5001) # default port is 5000