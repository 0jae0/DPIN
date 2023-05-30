from flask import *
import mya
import re

app = Flask(__name__)

education_offices = {
    '서울특별시교육청': 'B10',
    '부산광역시교육청': 'C10',
    '대구광역시교육청': 'D10',
    '인천광역시교육청': 'E10',
    '광주광역시교육청': 'F10',
    '대전광역시교육청': 'G10',
    '울산광역시교육청': 'H10',
    '세종특별자치시교육청': 'I10',
    '경기도교육청': 'J10',
    '강원도교육청': 'K10',
    '충청북도교육청': 'M10',
    '충청남도교육청': 'N10',
    '전라북도교육청': 'P10',
    '전라남도교육청': 'Q10',
    '경상북도교육청': 'R10',
    '경상남도교육청': 'S10',
    '제주특별자치도교육청': 'T10',
}

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal Server Error"}), 500
def validate_input(input_string):
    if re.match("^[A-Za-z0-9\uac00-\ud7a3]*$", input_string):
        return True
    else:
        return False
@app.route('/schedule/<string:EDU_NAME>/<string:SC_NAME>')
def sc(EDU_NAME, SC_NAME):
    if EDU_NAME in education_offices:
        SC_CODE = education_offices[EDU_NAME]
    else:
        return "Invalid input"
    if validate_input(SC_CODE) and validate_input(SC_NAME):
        return mya.schedule(SC_CODE, SC_NAME)
    else:
        return "Invalid input"
@app.route('/timetable/<string:EDU_NAME>/<string:SC_NAME>')
def tt(EDU_NAME, SC_NAME):
    if EDU_NAME in education_offices:
        SC_CODE = education_offices[EDU_NAME]
    else:
        return "Invalid input"
    if validate_input(SC_CODE) and validate_input(SC_NAME):
        return mya.timetable(SC_CODE, SC_NAME)
    else:
        return "Invalid input"
@app.route('/meal/<string:EDU_NAME>/<string:SC_NAME>')
def ml(EDU_NAME, SC_NAME):
    if EDU_NAME in education_offices:
        SC_CODE = education_offices[EDU_NAME]
    else:
        return "Invalid input"
    if validate_input(SC_CODE) and validate_input(SC_NAME):
        return mya.meal(SC_CODE, SC_NAME)
    else:
        return "Invalid input"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=32767)