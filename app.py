from flask import Flask, render_template, request
from aeroroute import aeroroute_input

app = Flask(__name__)

@app.route('/distance', methods=['GET', 'POST'])
def distancefinder():
    
    route = result = None
    
    if request.method == 'POST':
        route = request.form.get('route').upper()
        query = route.split()
        result = aeroroute_input(query)
    
    return render_template('distance.html', route=route, result=result)

@app.route('/cdr', methods=['GET', 'POST'])
def cdr():
    
    result = None
    departure = str()
    arrival = str()

    if request.method == 'POST':
        departure = request.form.get('departure')
        arrival = request.form.get('arrival')
        print(departure, arrival)
        result = ("place holder", departure, arrival)
    
    return render_template('cdr.html', departure=departure, arrival=arrival, result=result)

if __name__ == '__main__':
    app.run(debug=True)