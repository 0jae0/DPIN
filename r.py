from flask import *
import mya

app = Flask(__name__)
@app.route('/schedule')
def sc():
    return mya.schedule()

@app.route('/timetable')
def tt():
    return mya.timetable()
5
@app.route('/meal')
def ml():
    return mya.meal()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=32767)