import requests
import json
import datetime

keyfile = open('key.txt', 'r')
key = keyfile.read()
keyfile.close()

def checkdate():
    nowdate = datetime.datetime.now()
    year = nowdate.year
    month = nowdate.month
    month_str = "{:02d}".format(month)
    ym = str(year) + str(month_str)
    return ym  # 여기에서 'ym' 값을 반환합니다.

def schedule():
    ym = checkdate()  # 'ym' 값을 여기에서 받습니다.
    url = "https://open.neis.go.kr/hub/SchoolSchedule?KEY=" + key + "&ATPT_OFCDC_SC_CODE=D10&SD_SCHUL_CODE=7261025&AA_YMD=" + ym + "&Type=json"
    response = requests.get(url)
    json_data = json.loads(response.text)
    rows = json_data['SchoolSchedule'][1]['row']
    for row in rows:
        print(f'{row["AA_YMD"]} : {row["EVENT_NM"]}')

schedule()
