from flask import Flask
from aeroroute import main

app = Flask(__name__)

@app.route('/')
def index():
    # Call the main function from aeroroute.py
    result = main()

    # Return the result as a response
    return str(result)

if __name__ == '__main__':
    app.run()