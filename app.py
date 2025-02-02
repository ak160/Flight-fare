from flask import Flask, request, render_template
import pickle as pkl
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Load the model
with open('flight_model.pkl', 'rb') as file:
    model = pkl.load(file)

# Constants for mappings
ROUTE_MAPPING = {
    'BLR → DEL': 0,
            'CCU → IXR → BBI → BLR': 1,
            'DEL → LKO → BOM → COK': 2,
            'CCU → NAG → BLR': 3,
            'BLR → NAG → DEL': 4,
            'CCU → BLR': 5,
            'BLR → BOM → DEL': 6,
            'DEL → BOM → COK': 7,
            'DEL → BLR → COK': 8,
            'MAA → CCU': 9,
            'CCU → BOM → BLR': 10,
            'DEL → AMD → BOM → COK': 11,
            'DEL → PNQ → COK': 12,
            'DEL → CCU → BOM → COK': 13,
            'BLR → COK → DEL': 14,
            'DEL → IDR → BOM → COK': 15,
            'DEL → LKO → COK': 16,
            'CCU → GAU → DEL → BLR': 17,
            'DEL → NAG → BOM → COK': 18,
            'CCU → MAA → BLR': 19,
            'DEL → HYD → COK': 20,
            'CCU → HYD → BLR': 21,
            'DEL → COK': 22,
            'CCU → DEL → BLR': 23,
            'BLR → BOM → AMD → DEL': 24,
            'BOM → DEL → HYD': 25,
            'DEL → MAA → COK': 26,
            'BOM → HYD': 27,
            'DEL → BHO → BOM → COK': 28,
            'DEL → JAI → BOM → COK': 29,
            'DEL → ATQ → BOM → COK': 30,
            'DEL → JDH → BOM → COK': 31,
            'CCU → BBI → BOM → BLR': 32,
            'BLR → MAA → DEL': 33,
            'DEL → GOI → BOM → COK': 34,
            'DEL → BDQ → BOM → COK': 35,
            'CCU → JAI → BOM → BLR': 36,
            'CCU → BBI → BLR': 37,
            'BLR → HYD → DEL': 38,
            'DEL → TRV → COK': 39,
            'CCU → IXR → DEL → BLR': 40,
            'DEL → IXU → BOM → COK': 41,
            'CCU → IXB → BLR': 42,
            'BLR → BOM → JDH → DEL': 43,
            'DEL → UDR → BOM → COK': 44,
            'DEL → HYD → MAA → COK': 45,
            'CCU → BOM → COK → BLR': 46,
            'BLR → CCU → DEL': 47,
            'CCU → BOM → GOI → BLR': 48,
            'DEL → RPR → NAG → BOM → COK': 49,
            'DEL → HYD → BOM → COK': 50,
            'CCU → DEL → AMD → BLR': 51,
            'CCU → PNQ → BLR': 52,
            'BLR → CCU → GAU → DEL': 53,
            'CCU → DEL → COK → BLR': 54,
            'BLR → PNQ → DEL': 55,
            'BOM → JDH → DEL → HYD': 56,
            'BLR → BOM → BHO → DEL': 57,
            'DEL → AMD → COK': 58,
            'BLR → LKO → DEL': 59,
            'CCU → GAU → BLR': 60,
            'BOM → GOI → HYD': 61,
            'CCU → BOM → AMD → BLR': 62,
            'CCU → BBI → IXR → DEL → BLR': 63,
            'DEL → DED → BOM → COK': 64,
            'DEL → MAA → BOM → COK': 65,
            'BLR → AMD → DEL': 66,
            'BLR → VGA → DEL': 67,
            'CCU → JAI → DEL → BLR': 68,
            'CCU → AMD → BLR': 69,
            'CCU → VNS → DEL → BLR': 70,
            'BLR → BOM → IDR → DEL': 71,
            'BLR → BBI → DEL': 72,
            'BLR → GOI → DEL': 73,
            'BOM → AMD → ISK → HYD': 74,
            'BOM → DED → DEL → HYD': 75,
            'DEL → IXC → BOM → COK': 76,
            'CCU → PAT → BLR': 77,
            'BLR → CCU → BBI → DEL': 78,
            'CCU → BBI → HYD → BLR': 79,
            'BLR → BOM → NAG → DEL': 80,
            'BLR → CCU → BBI → HYD → DEL': 81,
            'BLR → GAU → DEL': 82,
            'BOM → BHO → DEL → HYD': 83,
            'BOM → JLR → HYD': 84,
            'BLR → HYD → VGA → DEL': 85,
            'CCU → KNU → BLR': 86,
            'CCU → BOM → PNQ → BLR': 87,
            'DEL → BBI → COK': 88,
            'BLR → VGA → HYD → DEL': 89,
            'BOM → JDH → JAI → DEL → HYD': 90,
            'DEL → GWL → IDR → BOM → COK': 91,
            'CCU → RPR → HYD → BLR': 92,
            'CCU → VTZ → BLR': 93,
            'CCU → DEL → VGA → BLR': 94,
            'BLR → BOM → IDR → GWL → DEL': 95,
            'CCU → DEL → COK → TRV → BLR': 96,
            'BOM → COK → MAA → HYD': 97,
            'BOM → NDC → HYD': 98,
            'BLR → BDQ → DEL': 99,
            'CCU → BOM → TRV → BLR': 100,
            'CCU → BOM → HBX → BLR': 101,
            'BOM → BDQ → DEL → HYD': 102,
            'BOM → CCU → HYD': 103,
            'BLR → TRV → COK → DEL': 104,
            'BLR → IDR → DEL': 105,
            'CCU → IXZ → MAA → BLR': 106,
            'CCU → GAU → IMF → DEL → BLR': 107,
            'BOM → GOI → PNQ → HYD': 108,
            'BOM → BLR → CCU → BBI → HYD': 109,
            'BOM → MAA → HYD': 110,
            'BLR → BOM → UDR → DEL': 111,
            'BOM → UDR → DEL → HYD': 112,
            'BLR → VGA → VTZ → DEL': 113,
            'BLR → HBX → BOM → BHO → DEL': 114,
            'CCU → IXA → BLR': 115,
            'BOM → RPR → VTZ → HYD': 116,
            'BLR → HBX → BOM → AMD → DEL': 117,
            'BOM → IDR → DEL → HYD': 118,
            'BOM → BLR → HYD': 119,
            'BLR → STV → DEL': 120,
            'CCU → IXB → DEL → BLR': 121,
            'BOM → JAI → DEL → HYD': 122,
            'BOM → VNS → DEL → HYD': 123,
            'BLR → HBX → BOM → NAG → DEL': 124,
            'BLR → BOM → IXC → DEL': 125,
            'BLR → CCU → BBI → HYD → VGA → DEL': 126,
            'BOM → BBI → HYD': 127
}

AIRLINE_MAPPING = {
            'IndiGo': 0,
            'Air India': 1,
            'Jet Airways': 2,
            'SpiceJet': 3,
            'Multiple carriers': 4,
            'GoAir': 5,
            'Vistara': 6,
            'Air Asia': 7,
            'Vistara Premium economy': 8,
            'Jet Airways Business': 9,
            'Multiple carriers Premium economy': 10,
            'Trujet': 11,
}

SOURCE_MAPPING = {
    'Banglore': 0,
    'Kolkata': 1,
    'Delhi': 2,
    'Chennai': 3,
    'Mumbai': 4,
}

DESTINATION_MAPPING = {
    'Delhi': 0,
    'Banglore': 1,
    'Cochin': 2,
    'Kolkata': 3,
    'Hyderabad': 5,
}

def get_route(source, destination, stops):
    for route, route_number in ROUTE_MAPPING.items():
        route_parts = route.split(' → ')
        if route_parts[0] == source and route_parts[-1] == destination and len(route_parts) - 2 == stops:
            return route, route_number
    return None, None

def preprocess_dates(dep_date, arr_date):
    dep_dt = datetime.strptime(dep_date, "%Y-%m-%dT%H:%M")
    arr_dt = datetime.strptime(arr_date, "%Y-%m-%dT%H:%M")
    
    journey_day = dep_dt.day
    journey_month = dep_dt.month
    dep_hour = dep_dt.hour
    dep_min = dep_dt.minute
    arr_hour = arr_dt.hour
    arr_min = arr_dt.minute
    dur_hour = abs(arr_hour - dep_hour)
    dur_min = abs(arr_min - dep_min)
    duration = dur_hour * 60 + dur_min
    
    return journey_day, journey_month, dep_hour, dep_min, arr_hour, arr_min, duration

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/myform', methods=['POST'])
def myform():
    try:
        # Extract form data
        dep_date = request.form['depart-date']
        arr_date = request.form['arrival-date']
        stops = int(request.form['stops'])
        airline = request.form['airline']
        source = request.form['departure'].split(" ")
        destination = request.form['arrival'].split(" ")

        # Preprocess dates
        journey_day, journey_month, dep_hour, dep_min, arr_hour, arr_min, duration = preprocess_dates(dep_date, arr_date)

        # Get route
        route_key, route = get_route(source[1], destination[1], stops)
        if route is None:
            return render_template('index.html', result='Route not found')

        # Map inputs
        source_num = SOURCE_MAPPING.get(source[0], -1)
        destination_num = DESTINATION_MAPPING.get(destination[0], -1)
        airline_num = AIRLINE_MAPPING.get(airline, -1)

        if -1 in (source_num, destination_num, airline_num):
            return render_template('index.html', result='Invalid source, destination, or airline')

        # Prepare input for model
        sample_input = pd.DataFrame({
            'Airline': [airline_num],
            'Source': [source_num],
            'Destination': [destination_num],
            'Route': [route],
            'Total_Stops': [stops],
            'Additional_Info': [8],
            'Duration': [duration],
            'Journey_day': [journey_day],
            'Journey_month': [journey_month],
            'Dep_hour': [dep_hour],
            'Dep_min': [dep_min],
            'Arrival_hour': [arr_hour],
            'Arrival_min': [arr_min]
        })

        # Predict price
        predicted_price = model.predict(sample_input)

        # Prepare result
        result = f"""
        <div class="output">
            <header><h2>Flight Details</h2></header>
            <div class="flight-output">
                <div class="inner-box"><p> Source: {source[0]}</p></div>
                <div class="inner-box"><p> Destination: {destination[0]}</p></div>
                <div class="inner-box"><p> Airline: {airline}</p></div>
                <div class="inner-box"><p> Route: {route_key}</p></div>
                <div class="inner-box"><p> Duration: {duration}</p></div>
                <div class="inner-box"><p> Predicted Price: {predicted_price[0]}</p></div>
            </div>
        </div>
        """

        return render_template('index.html', result=result)

    except Exception as e:
        return render_template('index.html', result=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)