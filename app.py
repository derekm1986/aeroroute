from flask import Flask, render_template
from aeroroute import aeroroute_input

app = Flask(__name__)

@app.route('/')
def index():
    # Call the main function from aeroroute.py
    result = aeroroute_input(("KJFK", "EGLL"))

    # Return the result as a response
    #return str(result)
    
    # Render the index.html template and pass the result to it
    return f"Result from aeroroute.py: {result}"

if __name__ == '__main__':
    app.run(debug=True)