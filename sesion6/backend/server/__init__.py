from flask import (
    Flask,
    abort,
    jsonify,
    request
)
from flask_cors import CORS
from models import setup_db, Todo, TodoList

TODOS_PER_PAGE=5

def paginate_todos(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1)*TODOS_PER_PAGE
    end = start + TODOS_PER_PAGE
    todos = [todo.format() for todo in selection]
    current_todos = todos[start:end]
    return current_todos

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    # CORS(app) = CORS(app, "*")
    CORS(app)
    #CORS(app, origins=['https://utec.edu.pe', 'http://127.0.0.1:5001'], max_age=10)

    @app.after_request
    def after_requests(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorizations, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/todos', methods=['GET'])
    def get_todos():
        selection = Todo.query.order_by('id').all()
        todos = paginate_todos(request, selection)

        if len(todos) == 0:
            abort(404)
        
        return jsonify({
            'success': True,
            'todos': todos,
            'total_todos': len(selection)
        })
    
    @app.route('/todos', methods=['POST'])
    def create_todo():
        body = request.get_json()

        description = body.get('description', None)
        completed = body.get('completed', None)
        list_id = body.get('list_id', None)

        todo = Todo(description=description, completed=completed, list_id=list_id)
        todo.insert()
        new_todo_id = todo.id

        selection = Todo.query.order_by('id').all()
        todos = paginate_todos(request, selection)

        return jsonify({
            'success': True,
            'created': new_todo_id,
            'todos': todos,
            'total_todos': len(selection)
        })
    
    @app.route('/todos/<todo_id>', methods=['PATCH'])
    def update_todo(todo_id):
        todo = Todo.query.filter(Todo.id==todo_id).one_or_none()

        if todo is None:
            abort(404)
        
        body = request.get_json()
        if 'description' in body:
            todo.description = body.get('description')
        
        todo.update()

        return jsonify({
            'success': True,
            'id': todo.id
        })
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'code': 404,
            'message': 'resource not found'
        }), 404
    
    return app
