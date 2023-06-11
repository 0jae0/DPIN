import requests
import json
import datetime

keyfile = open('key.txt', 'r')
key = keyfile.read()
keyfile.close()


def info(sc_code, sc_name):
    global sd_schul_code
    url = "https://open.neis.go.kr/hub/schoolInfo?KEY=" + key + "&ATPT_OFCDC_sc_code=" + sc_code + "&SCHUL_NM=" + sc_name + "&Type=json"
    response = requests.get(url)
    json_data = json.loads(response.text)
    rows = json_data['schoolInfo'][1]['row']
    for row in rows:
        sd_schul_code = row['SD_SCHUL_CODE']
    return sd_schul_code


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


def schedule(sc_code, sc_name):
    sd_schul_code = info(sc_code, sc_name)
    print(sd_schul_code)
    result = str("")
    ym = checkym()  # yearmonth get
    url = "https://open.neis.go.kr/hub/SchoolSchedule?KEY=" + key + "&ATPT_OFCDC_SC_CODE=" + sc_code + "&SD_SCHUL_CODE=" + sd_schul_code + "&AA_YMD=" + str(
        ym) + "&Type=json"
    response = requests.get(url)
    json_data = json.loads(response.text)
    rows = json_data['SchoolSchedule'][1]['row']
    result += "{"
    atpt_metropolitan_name = [""]
    for row in rows:
        atpt_metropolitan_name += f'"{row["ATPT_OFCDC_SC_NM"]}'
    for row in rows:
        result += f'"{row["AA_YMD"]} {row["EVENT_NM"]}", '
    result += "}"
    print(result)
    return result


def timetable(sc_code, sc_name):
    SD_SCHUL_CODE = info(sc_code, sc_name)
    result = str("")
    ymd = checkymd()
    url = "https://open.neis.go.kr/hub/misTimetable?KEY=" + key + "&ATPT_OFCDC_sc_code=" + sc_code + "&SD_SCHUL_CODE=" + SD_SCHUL_CODE + "&GRADE=3&CLASS_NM=4&ALL_TI_YMD=" + ymd + "&Type=json"
    response = requests.get(url)
    json_data = json.loads(response.text)
    rows = json_data['misTimetable'][1]['row']
    result += "{" + f'"학년" : "{rows[0]["GRADE"]}", "반" : "{rows[0]["CLASS_NM"]}", "과목" : "'
    for row in rows:
        result += f'{row["ITRT_CNTNT"].replace("-", " ")}'
    result += '"}'
    return result


def meal(sc_code, sc_name):
    SD_SCHUL_CODE = info(sc_code, sc_name)
    result = str("")
    ymd = checkymd()
    url = "https://open.neis.go.kr/hub/mealServiceDietInfo?KEY=" + key + "&ATPT_OFCDC_sc_code=" + sc_code + "&SD_SCHUL_CODE=" + SD_SCHUL_CODE + "&MLSV_YMD=" + ymd + "&Type=json"
    response = requests.get(url)
    json_data = json.loads(response.text)
    rows = json_data['mealServiceDietInfo'][1]['row']
    for row in rows:
        result += "{" + f'"식사구분" : "{row["MMEAL_SC_NM"]}", "메뉴" : "{row["DDISH_NM"].replace("<br/>", "").replace("11", "복숭아.").replace("10.", "돼지고기.").replace("12.", "토마토.").replace("13.", "아황산류.").replace("14.", "호두.").replace("15.", "닭고기.").replace("16.", "쇠고기.").replace("17.", "오징어.").replace("18.", "조개류.").replace("1.", "난류.").replace("2.", "우유.").replace("3.", "메밀.").replace("4.", "땅콩.").replace("5.", "대두.").replace("6.", "밀.").replace("7.", "고등어.").replace("8.", "게.").replace("9.", "새우.").replace(" ", "").replace(")", ") ")}", "칼로리" : "{row["CAL_INFO"]}"' + "}"
    return result

if schedule("B10", "서울대학교사범대학부설중학교") != "Internal Server Error":
    if timetable("B10", "서울대학교사범대학부설중학교") != "Internal Server Error":
        if meal("B10", "서울대학교사범대학부설중학교") != "Internal Server Error":
            print("BACK READY")
else:
    exit()