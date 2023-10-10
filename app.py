import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Create an SQLAlchemy engine to connect to your SQLite database
engine = create_engine("sqlite:///data/name_db.sqlite")

# Reflect the database tables into SQLAlchemy ORM classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# Create references to the tables in the database
BabyNameData = Base.classes.baby_name_data

# Create a Flask app
app = Flask(__name__)

# Create a route to list all available API endpoints
@app.route("/")
def welcome():
    return (
        "Welcome to the Baby Names API!<br/>"
        "Available Routes:<br/>"
        "/api/v1.0/all<br/>"
        "/api/v1.0/<year>/<gender>"
    )

# Create a route to get all popular baby names from boys & girls (1980 - 2022)
@app.route("/api/v1.0/all")
def boys_girls_all():
    session = Session(engine)
    
    # Query all popular baby names
    results = session.query(BabyNameData).all()
    
    session.close()
    
    # Convert the results to a list of dictionaries
    baby_names_list = []
    for result in results:
        baby_names_list.append({
            "year": result.year,
            "name": result.name,
            "gender": result.gender,
            "count": result.count
        })
    
    return jsonify(baby_names_list)

# Create a route to get popular baby names for a specific year and gender
@app.route("/api/v1.0/<year>/<gender>")
def names_filtered(year, gender):
    session = Session(engine)
    
    # Query popular baby names for the specified year and gender
    results = session.query(BabyNameData).filter_by(year=year, gender=gender).all()
    
    session.close()
    
    # Convert the results to a list of dictionaries
    baby_names_list = []
    for result in results:
        baby_names_list.append({
            "year": result.year,
            "name": result.name,
            "gender": result.gender,
            "count": result.count
        })
    
    return jsonify(baby_names_list)

if __name__ == '__main__':
    app.run(debug=True)








