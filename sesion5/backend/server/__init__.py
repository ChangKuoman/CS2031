from flask import (
    Flask,
    abort,
    jsonify
)
from flask_cors import CORS
from models import setup_db, Todo, TodoList

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_requests(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorizations, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/todos', methods=['GET'])
    def get_todos():
        todos = Todo.query.order_by('id').all()

        if len(todos) == 0:
            abort(404)
        
        return jsonify({
            'success':True,
            'todos':[todo.format() for todo in todos],
            'total_todos':len(todos)
        })
    
    return app
