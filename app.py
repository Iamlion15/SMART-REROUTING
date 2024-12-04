from flask import Flask, render_template, request
from SCRIPT.AI_project import find_optimal_path


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
        result = find_optimal_path( origin, destination)  
        if result==None:
            print("nooooooooooooooooooooooooo") 
            return render_template('noDataFound.html')
        else:    
            print('------------result-------------')
            print(result[0])
            return render_template('rerouteResult.html',dataFound="yes", optimal_path=result[0],all_routes=result[2],optimal_score=result[1],origin=origin,destination=destination)
    

if __name__ == '__main__':
    app.run(debug=True,port=7000)
