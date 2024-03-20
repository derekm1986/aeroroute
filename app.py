from flask import Flask, render_template
from aeroroute import flask_test

app = Flask(__name__)

@app.route('/')
def index():
    # Call the main function from aeroroute.py
    result = flask_test()

    # Return the result as a response
    #return str(result)
    
    # Render the index.html template and pass the result to it
    return render_template('index.html', result=result)

print(index())

if __name__ == '__main__':
    print("Got here!")
    app.run()