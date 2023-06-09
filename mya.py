import requests
import json
import datetime
import random

keyfile = open('key.txt', 'r')
key = keyfile.read()
keyfile.close()
def info(SC_CODE, SC_NAME):
    url = "https://open.neis.go.kr/hub/schoolInfo?KEY=" + key + "&ATPT_OFCDC_SC_CODE=" + SC_CODE + "&SCHUL_NM=" + SC_NAME + "&Type=json"
    response = requests.get(url)
    json_data = json.loads(response.text)
    rows = json_data['schoolInfo'][1]['row']
    for row in rows:
        SD_SCHUL_CODE = row['SD_SCHUL_CODE']
    return SD_SCHUL_CODE

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

def schedule(SC_CODE, SC_NAME):
    SD_SCHUL_CODE = info(SC_CODE, SC_NAME)
    result = str("")
    ym = checkym()
    url = "https://open.neis.go.kr/hub/SchoolSchedule?KEY=" + key + "&ATPT_OFCDC_SC_CODE=" + SC_CODE + "&SD_SCHUL_CODE="  + SD_SCHUL_CODE + "&AA_YMD=" + str(ym) + "&Type=json"
    response = requests.get(url)
    json_data = json.loads(response.text)
    rows = json_data['SchoolSchedule'][1]['row']
    result += "["
    for row in rows:
        result += f'"{row["AA_YMD"]} {row["EVENT_NM"]}", '
    result += "]"
    return result

def timetable(SC_CODE, SC_NAME):
    SD_SCHUL_CODE = info(SC_CODE, SC_NAME)
    result = str("")
    ymd=checkymd()
    url = "https://open.neis.go.kr/hub/misTimetable?KEY=" + key + "&ATPT_OFCDC_SC_CODE=" + SC_CODE + "&SD_SCHUL_CODE=" + SD_SCHUL_CODE + "&GRADE=3&CLASS_NM=4&ALL_TI_YMD=" + ymd + "&Type=json"
    response = requests.get(url)
    json_data = json.loads(response.text)
    rows = json_data['misTimetable'][1]['row']
    result += "{" + f'"학년" : "{rows[0]["GRADE"]}", "반" : "{rows[0]["CLASS_NM"]}", "과목" : "'
    for row in rows:
        result += f'{row["ITRT_CNTNT"].replace("-", " ")}'
    result += '"}'
    return result

def meal(SC_CODE, SC_NAME):
    SD_SCHUL_CODE = info(SC_CODE, SC_NAME)
    result = str("")
    ymd=checkymd()
    url = "https://open.neis.go.kr/hub/mealServiceDietInfo?KEY=" + key + "&ATPT_OFCDC_SC_CODE=" + SC_CODE + "&SD_SCHUL_CODE="  + SD_SCHUL_CODE + "&MLSV_YMD=" + ymd + "&Type=json"
    response = requests.get(url)
    json_data = json.loads(response.text)
    print(json_data)
    rows = json_data['mealServiceDietInfo'][1]['row']
    for row in rows:
        result += "{" + f'"식사구분" : "{row["MMEAL_SC_NM"]}", "메뉴" : "{row["DDISH_NM"].replace("<br/>", "").replace("11", "복숭아.").replace("10.", "돼지고기.").replace("12.", "토마토.").replace("13.", "아황산류.").replace("14.", "호두.").replace("15.", "닭고기.").replace("16.", "쇠고기.").replace("17.", "오징어.").replace("18.", "조개류.").replace("1.", "난류.").replace("2.", "우유.").replace("3.", "메밀.").replace("4.", "땅콩.").replace("5.", "대두.").replace("6.", "밀.").replace("7.", "고등어.").replace("8.", "게.").replace("9.", "새우.").replace(" ", "").replace(")", ") ")}", "칼로리" : "{row["CAL_INFO"]}"' + "}"
    return result

def hantemp():
    url = "https://api.hangang.msub.kr/"
    response = requests.get(url)
    json_data = json.loads(response.text)
    #{'station': '노량진', 'status': 'success', 'temp': '20.0', 'time': '12:00', 'type': 'hangangAPI'}
    result = str("")
    result += "{" + f'"강이름" : "{json_data["station"]}", "온도" : "{json_data["temp"]}", "시간" : "{json_data["time"]}", "명언" : ' + goodtext() + "}"
    return result

def goodtext():
    r = random.randrange(1, 11)
    if r == 1:
        return("인생 살만한듯?")
    if r == 2:
        return("힘내라")
    if r == 3:
        return("알빠노")
    else:
        return("나머지는 귀찮은데 일단 API 이따 씀")
    # 명언을 딱 갖다주는 API가 업어서 일단 이렇게 랜덤으로 주기는 했는데 나중에 API로 줄거임
