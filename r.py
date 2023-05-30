from flask import *
import mya
import re

app = Flask(__name__)
@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal Server Error"}), 500
def validate_input(input_string):
    if re.match("^[A-Za-z0-9]*$", input_string):
        return True
    else:
        return False
@app.route('/schedule/<string:SC_CODE>/<string:SC_NAME>')
def sc(SC_CODE, SC_NAME):
    if validate_input(SC_CODE) and validate_input(SC_NAME):
        return mya.schedule(SC_CODE, SC_NAME)
    else:
        return "Invalid input"
@app.route('/timetable/<string:SC_CODE>/<string:SC_NAME>')
def tt(SC_CODE, SC_NAME):
    if validate_input(SC_CODE) and validate_input(SC_NAME):
        return mya.timetable(SC_CODE, SC_NAME)
    else:
        return "Invalid input"
@app.route('/meal/<string:SC_CODE>/<string:SC_NAME>')
def ml(SC_CODE, SC_NAME):
    if validate_input(SC_CODE) and validate_input(SC_NAME):
        return mya.meal(SC_CODE, SC_NAME)
    else:
        return "Invalid input"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=32767)