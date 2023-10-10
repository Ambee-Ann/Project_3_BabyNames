import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect 
import os

from flask import Flask, jsonify

db_path = os.path.join(os.path.dirname(__file__), 'data', 'names_data.db')

engine = create_engine(f'sqlite:///{db_path}')
# engine = create_engine('sqlite:////data/name_data.db')
Base = automap_base()
Base.prepare(autoload_with=engine)

Names = Base.classes.baby_names

session = Session(engine)
app = Flask(__name__)

#--------------------------------------
# Flask Routes
#--------------------------------------
@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"Top 5 Baby Names From Each State :<br/>"
        f"All Popular Baby Names From Boys & Girls (1980 - 2022): api/v1.0/all<br/>"
        f"Popular Baby Names By Year and Gender (1980- 2022): api/v1.0/<year>/<gender> <br/>"
    )

@app.route("/api/v1.0/all")
def boys_girls_all():
    """list of all popular baby names from boys & girls (1980 - 2022)"""
    # Query names from boys & girls
    boys_girls = session.query(Names).all()
    session.close()
    return jsonify(boys_girls)

# Create a route that queries all popular baby names for selected year/gender.
@app.route("/api/v1.0/<year>/<gender>")
def names_filtered(year, gender):
    """List of all popular baby names from boys (1980- 2022)"""
    # Query names from boys & girls
    results = session.query(Names).filter(Names.year == year).filter(Names.Gender == gender).all()
    session.close()
    return jsonify(results)

if __name__ == '__main__':
    app.run()