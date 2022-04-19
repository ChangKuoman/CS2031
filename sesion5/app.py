# imports
from flask import Flask, render_template


# configurations
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', data=[
        {
            'description':'todo 1'
        },
        {
            'description':'todo 2'
        },
        {
            'description':'todo 3'
        },
        {
            'description':'todo 4'
        }
    ])

# run
if __name__ == '__main__':
    app.run(debug=True, port=5000)
