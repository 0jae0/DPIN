from flask import *
import mya
import random
import re
import time

app = Flask(__name__)

education_offices = {
    "B10": ["서울", "서울시", "서울교육청", "서울시교육청", "서울특별시", "서울특별시교육청"],
    "C10": ["부산", "부산광역시", "부산시", "부산교육청", "부산광역시교육청"],
    "D10": ["대구", "대구광역시", "대구시", "대구교육청", "대구광역시교육청", "홍준표"],
    "E10": ["인천", "인천광역시", "인천시", "인천교육청", "인천광역시교육청"],
    "F10": ["광주", "광주광역시", "광주시", "광주교육청", "광주광역시교육청"],
    "G10": ["대전", "대전광역시", "대전시", "대전교육청", "대전광역시교육청"],
    "H10": ["울산", "울산광역시", "울산시", "울산교육청", "울산광역시교육청"],
    "I10": ["세종", "세종특별시", "세종시", "세종교육청", "세종특별자치시", "세종특별자치시교육청"],
    "J10": ["경기", "경기도", "경기교육청", "경기도교육청"],
    "K10": ["강원", "강원도", "강원교육청", "강원도교육청"],
    "M10": ["충북", "충청북도", "충북교육청", "충청북도교육청"],
    "N10": ["충남", "충청남도", "충남교육청", "충청남도교육청"],
    "P10": ["전북", "전라북도", "전북교육청", "전라북도교육청"],
    "Q10": ["전남", "전라남도", "전남교육청", "전라남도교육청"],
    "R10": ["경북", "경상북도", "경북교육청", "경상북도교육청"],
    "S10": ["경남", "경상남도", "경남교육청", "경상남도교육청"],
    "T10": ["제주", "제주도", "제주특별자치시", "제주교육청", "제주도교육청", "제주특별자치시교육청", "제주특별자치도", "서귀포"],
}

def get_code_from_name(name):
    for code, names in education_offices.items():
        if name in names:
            return code
    return None

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal Server Error"}), 500

def validate_input(input_string):
    if re.match("^[A-Za-z0-9\uac00-\ud7a3]*$", input_string):
        return True
    else:
        return False

@app.route('/schedule/<string:edu_name>/<string:sc_name>')
def sc(edu_name, sc_name):
    sc_code = get_code_from_name(edu_name)
    if sc_code is None:
        return "Invalid input"
    if validate_input(sc_code) and validate_input(sc_name):
        return jsonify(mya.schedule(sc_code, sc_name))
    else:
        return "Invalid input"

@app.route('/timetable/<string:edu_name>/<string:sc_name>')
def tt(edu_name, sc_name):
    sc_code = get_code_from_name(edu_name)
    if sc_code is None:
        return "Invalid input"
    if validate_input(sc_code) and validate_input(sc_name):
        return jsonify(mya.timetable(sc_code, sc_name))
    else:
        return "Invalid input"

@app.route('/meal/<string:edu_name>/<string:sc_name>')
def ml(edu_name, sc_name):
    sc_code = get_code_from_name(edu_name)
    if sc_code is None:
        return "Invalid input"
    if validate_input(sc_code) and validate_input(sc_name):
        return jsonify(mya.meal(sc_code, sc_name))
    else:
        return "Invalid input"

if __name__ == "__main__":
    print("FLASK READY")
    time.sleep(0.3)
    print("IGNITION")
app.run(host='0.0.0.0', port=32767)
