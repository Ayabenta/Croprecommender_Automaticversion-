import pickle 
from flask import Flask, jsonify, request
import pandas as pd 
import pyrebase 
config = {
    "apiKey": "AIzaSyDJM6U2PhmhURsYaBOFZ-mWJO4rn5GhKL8",
    "authDomain": "highagriv6.firebaseapp.com",
    "databaseURL": "https://highagriv6-default-rtdb.firebaseio.com",
    "projectId": "highagriv6",
    "storageBucket": "highagriv6.appspot.com",
    "messagingSenderId": "902180705852",
    "appId": "1:902180705852:web:893176f34cffa29909d539"}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()

#load model 
model = pickle.load(open('croprecommenderv1.pkl', 'rb'))
#Create App
app = Flask(__name__)
@app.route('/', methods = ['GET'])
#app.route("/") this tells flask what url should trigger our function in my 
# case / means my localhost 
def predict():
    data =  {'N' : list(dict(database.child("").child("nitrogen_value").get().val()).values())[-1],
 'P': list(dict(database.child("").child("phosphorous_value").get().val()).values())[-1],
 'K': list(dict(database.child("").child("potassium_value").get().val()).values())[-1],
 'humidity': list(dict(database.child("").child("air_humidity").get().val()).values())[-1],
 'ph': list(dict(database.child("").child("soil_ph").get().val()).values())[-1],
 'temperature': list(dict(database.child("").child("air_temperature").get().val()).values())[-1]
}
    data.update((x,[y]) for x,y in data.items())
    data_df = pd.DataFrame.from_dict(data)
    result = model.predict(data_df)
    output = result[0] 
    return jsonify(output)
if __name__ == '__main__':
    app.run(debug=True)


