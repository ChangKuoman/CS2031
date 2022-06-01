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

# configurations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/todoappdbp10'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# models
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__(self):
        return f'Todo: id={self.id}, description={self.description}'

class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list', lazy=True)

    def __repr__(self):
        return f'TodoList: id={self.id}, description={self.description}'

#db.create_all()


# controllers
@app.route('/lists/create', methods=['POST', 'GET'])
def create_list():
    response = {}
    try:
        name = request.get_json()['name']
        list = TodoList(name=name)
        db.session.add(list)
        db.session.commit()
        response['id'] = list.id
        response['name'] = name
    except Exception as e:
        print(e)
        db.session.rollback()
    finally:
        db.session.close()

    return jsonify(response)


@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    return render_template(
        'index.html',
        todos=Todo.query.filter_by(list_id=list_id).order_by('id').all(),
        current_list=TodoList.query.get(list_id),
        lists=TodoList.query.all()
        )

@app.route('/todos/<todo_id>/delete-todo', methods=['DELETE'])
def delete_todo(todo_id):
    response = {}
    try:
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        # Todo.query.delete()
        db.session.commit()
        response['id'] = todo.id
        response['success'] = True
    except Exception as e:
        print(e)
        db.session.rollback()
        response['success'] = False
    finally:
        db.session.close()
    return jsonify(response)

@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))


@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    response = {}
    try:
        description = request.get_json()['description']
        item_id = request.get_json()['item_id']
        todo = Todo(description=description, list_id=item_id)
        db.session.add(todo)
        db.session.commit()
        response['description'] = description
    except Exception as e:
        error = True
        print(e)
        db.session.rollback()
    finally:
        db.session.close()
    
    if error:
        abort(500)
    else:
        return jsonify(response)


@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def update_completed(todo_id):
    # elegante por path parameter solo pasar como maximo 2 parametros
    try:
        print("halo")
        new_completed = request.get_json()['new_completed']
        todo = Todo.query.get(todo_id)
        todo.completed = new_completed
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        print(e)
        print(sys.exs_info())
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todos/create', methods=['GET'])
def create_todo_get():
    try:
        description = request.args.get('description', '')
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
    except Exception as e:
        print(e)
        print(sys.exs_info())
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))


# run
if __name__ == '__main__':
    app.run(debug=True, port=5000)