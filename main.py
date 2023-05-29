import requests
import json
import datetime

keyfile = open('key.txt', 'r')
key = keyfile.read()
keyfile.close()

def checkym():
    nowdate = datetime.datetime.now()
    year = nowdate.year
    month = nowdate.month
    month_str = "{:02d}".format(month)
    ym = str(year) + str(month_str)
    return ym

def checkymd():
    nowdate = datetime.datetime.now()
    year = nowdate.year
    month = nowdate.month
    month_str = "{:02d}".format(month)
    day = nowdate.day
    day_str = "{:02d}".format(day)
    ymd = str(year) + str(month_str) + str(day_str)
    return ymd

def schedule():
    ym = checkym()  # 'ym' 값을 여기에서 받습니다.
    url = "https://open.neis.go.kr/hub/SchoolSchedule?KEY=" + key + "&ATPT_OFCDC_SC_CODE=D10&SD_SCHUL_CODE=7261025&AA_YMD=" + ym + "&Type=json"
    response = requests.get(url)
    json_data = json.loads(response.text)
    rows = json_data['SchoolSchedule'][1]['row']
    for row in rows:
        print(f'{row["AA_YMD"]} : {row["EVENT_NM"]}')

def timetable():
    ymd=checkymd()
    url = "https://open.neis.go.kr/hub/misTimetable?KEY=" + key + "&ATPT_OFCDC_SC_CODE=D10&SD_SCHUL_CODE=7261025&GRADE=3&CLASS_NM=4&ALL_TI_YMD=" + ymd + "&Type=json"
    response = requests.get(url)
    json_data = json.loads(response.text)
    rows = json_data['misTimetable'][1]['row']
    for row in rows:
        print(f'{row["PERIO"]} : {row["ITRT_CNTNT"]} : {row["GRADE"]}학년 {row["CLASS_NM"]}반')


timetable()
schedule()