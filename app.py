
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



# Database Setup
#################################################
engine = create_engine("sqlite:///data/name_data.sqlite")
Base = automap_base()
Base.prepare(engine, reflect= True)
Names = Base.classes.name_data

session = Session(engine)
app = Flask(__name__)

# Define a route to serve the HTML page
#@app.route('/')
#def Welcome():
    #return render_template('index.html')

    

# Define a route to serve static files (e.g., CSS and JavaScript)
#@app.route('/static/<path:filename>')
#def static_files(filename):
#    return send_from_directory('static', filename)


#--------------------------------------
# Flask Routes
#--------------------------------------
@app.route("/")
def welcome():
    """List all available api routes."""
    return(
        f"Top 5 Baby Names From Each State  :<br/>"
        f"All Popular Baby Names From Boys & Girls (1980 - 2022): api/v1.0/all<br/>"
        f"Popular Baby Names By year and Gender (1980- 2022): api/v1.0/<year>/<gender> <br/>"
    )
# Create a route that queries all popular baby names from boys & girls (1980 - 2022) and returns a dictionary.
@app.route("/api/v1.0/all")
def boys_girls_all():
    """list of all popular baby names from boys & girls (1980 - 2022)"""
    # Query names from boys & girls
    boys_girls = session.query(Names).all()
    session.close()
    return jsonify(boys_girls)
# Create a route that queries all popular baby names from boys (1980 - 2022).
@app.route("api/v1.0/<year>/<gender>")
def names_filtered(year, gender):
    """List of all popular baby names from boys (1980- 2022)"""
    # Query names from boys & girls
    results = session.query(Names).filter(Names.year == year).filter(Names.Gender == gender).all()
    session.close()
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)











