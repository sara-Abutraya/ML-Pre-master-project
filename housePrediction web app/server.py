from flask import Flask, request, render_template

from util import load_saved_objects, predict_price

app = Flask(__name__)


@app.route('/')
def hello():
    price = 0
    return render_template('index.html', price=price)


@app.route('/predicted_price',methods = ['POST', 'GET'])
def print_data():
    price = 0

    if request.method == 'POST':
        Address = request.values.get('address')
        Rooms = request.values.get('Rooms')
        Bathrooms = request.values.get('Bathrooms')
        Area = request.values.get('Area')
        Floor = request.values.get('Floor')
        Finishing_type = request.values.get('Finishing_type')
        Overlooking = request.values.get('Overlooking')

        year_built = request.values.get('age')
        age = 2021 - int(year_built)
        price = predict_price(Address, Rooms, Bathrooms, Area, Floor, age, Finishing_type, Overlooking)

    return render_template('index.html', price=price)


if __name__ == "__main__":
    load_saved_objects()
    app.run(debug=True)