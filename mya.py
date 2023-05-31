import requests
import json
import datetime

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
    ym = checkym()  # 'ym' 값을 여기에서 받습니다.
    url = "https://open.neis.go.kr/hub/SchoolSchedule?KEY=" + key + "&ATPT_OFCDC_SC_CODE=" + SC_CODE + "&SD_SCHUL_CODE="  + SD_SCHUL_CODE + "&AA_YMD=" + str(ym) + "&Type=json"
    response = requests.get(url)
    json_data = json.loads(response.text)
    rows = json_data['SchoolSchedule'][1]['row']
    for row in rows:
        result += "{" + f'"{row["AA_YMD"]}" : "{row["EVENT_NM"]}"' + "}"
    return result

def timetable(SC_CODE, SC_NAME):
    SD_SCHUL_CODE = info(SC_CODE, SC_NAME)
    result = str("")
    ymd=checkymd()
    url = "https://open.neis.go.kr/hub/misTimetable?KEY=" + key + "&ATPT_OFCDC_SC_CODE=" + SC_CODE + "&SD_SCHUL_CODE="  + SD_SCHUL_CODE + "&GRADE=3&CLASS_NM=4&ALL_TI_YMD=" + ymd + "&Type=json"
    response = requests.get(url)
    json_data = json.loads(response.text)
    rows = json_data['misTimetable'][1]['row']
    for row in rows:
        result += "{" + f'"{row["PERIO"]}" : "{row["ITRT_CNTNT"]}" : "{row["GRADE"]}학년" "{row["CLASS_NM"]}"' + "}"
    return result

def meal(SC_CODE, SC_NAME):
    SD_SCHUL_CODE = info(SC_CODE, SC_NAME)
    result = str("")
    ymd=checkymd()
    url = "https://open.neis.go.kr/hub/mealServiceDietInfo?KEY=" + key + "&ATPT_OFCDC_SC_CODE=" + SC_CODE + "&SD_SCHUL_CODE="  + SD_SCHUL_CODE + "&MLSV_YMD=" + ymd + "&Type=json"
    response = requests.get(url)
    json_data = json.loads(response.text)
    rows = json_data['mealServiceDietInfo'][1]['row']
    for row in rows:
        result += "{" + f'"{row["MMEAL_SC_NM"]}" : "{row["CAL_INFO"]}" : "{row["DDISH_NM"].replace("<br/>", "").replace("11", "복숭아.").replace("10.", "돼지고기.").replace("12.", "토마토.").replace("13.", "아황산류.").replace("14.", "호두.").replace("15.", "닭고기.").replace("16.", "쇠고기.").replace("17.", "오징어.").replace("18.", "조개류.").replace("1.", "난류.").replace("2.", "우유.").replace("3.", "메밀.").replace("4.", "땅콩.").replace("5.", "대두.").replace("6.", "밀.").replace("7.", "고등어.").replace("8.", "게.").replace("9.", "새우.")}"' + "}"
    return result