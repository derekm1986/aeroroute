from flask import Flask, render_template, request
from aeroroute import aeroroute_input
from cdrgetter import cdr_finder_dep_arr

app = Flask(__name__)

@app.route('/distance', methods=['GET', 'POST'])
def distancefinder():
    
    route = result = None
    
    if request.method == 'POST':
        route = request.form.get('route').upper()
        result = aeroroute_input(route)
    
    return render_template('distance.html', route=route, result=result)

@app.route('/cdr', methods=['GET', 'POST'])
def cdr():
    
    result = None
    departure = str()
    arrival = str()

    if request.method == 'POST':
        result = None
        departure = request.form.get('departure').upper()
        arrival = request.form.get('arrival').upper()
        result = cdr_finder_dep_arr(departure, arrival)
    
    return render_template('cdr.html', departure=departure, arrival=arrival, result=result)

if __name__ == '__main__':
    app.run(debug=True)
    