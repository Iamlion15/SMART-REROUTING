from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check-route', methods=['GET', 'POST'])
def routeOperations():
    return render_template('routeOperations.html')

@app.route('/route', methods=['GET', 'POST'])
def route():
    if request.method == 'GET':
        # origin = request.form['origin']
        # destination = request.form['destination']
        origin = request.args.get('origin')
        destination = request.args.get('destination')
        best_route = f"The best route from {origin} to {destination}"     
        return render_template('rerouteResult.html', best_route=best_route)
    

if __name__ == '__main__':
    app.run(debug=True,port=7000)
