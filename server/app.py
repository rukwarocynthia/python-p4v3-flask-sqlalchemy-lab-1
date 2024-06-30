# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    earthquake = db.session.get(Earthquake, id)
    if not earthquake: 
        # return {f"message": "Earthquake {id} not found."}, 404
        return {"message": f"Earthquake {id} not found."}, 404
    return(earthquake.to_dict()), 200

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquake_by_mangnitude(magnitude):
    earthquakes = []
    for earthquake in Earthquake.query.filter(Earthquake.magnitude >= magnitude).all():
        earthquakes.append(earthquake.to_dict())
    body = {
        'count' : len(earthquakes),
        'quakes' : earthquakes
    }

    return body, 200

# Add views here


if __name__ == '__main__':
    app.run(port=5555, debug=True)
