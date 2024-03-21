from flask import Flask, render_template, request
from aeroroute import aeroroute_input

app = Flask(__name__)

# @app.route('/')
# def index():
#     # Call the main function from aeroroute.py
    
#     query = ("KJFK", "EGLL")

#     result = aeroroute_input((query))

#     # Return the result as a response
#     #return str(result)
    
#     # Render the index.html template and pass the result to it
#     return render_template('index.html', query=query, result=result)
    
    
#     #return f"Result from aeroroute.py: {result}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        route = request.form.get('route').upper()
        query = (route.split())
        result = aeroroute_input(query)
        return render_template('result.html', route=route, result=result)
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)