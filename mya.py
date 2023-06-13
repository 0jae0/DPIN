import requests
import json
import datetime

try:
    with open('key.txt', 'r') as keyfile:
        key = keyfile.read()
except FileNotFoundError:
    print("key.txt file does not exist.")
    exit(1)
except IOError:
    print("Error occurred while trying to read key.txt")
    exit(1)

def info(sc_code, sc_name):
    global sd_schul_code
    url = "https://open.neis.go.kr/hub/schoolInfo?KEY=" + key + "&ATPT_OFCDC_SC_CODE=" + sc_code + "&SCHUL_NM=" + sc_name + "&Type=json"
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
    ym = checkym()
    url = "https://open.neis.go.kr/hub/SchoolSchedule?KEY=" + key + "&ATPT_OFCDC_SC_CODE=" + sc_code + "&SD_SCHUL_CODE=" + sd_schul_code + "&AA_YMD=" + str(
        ym) + "&Type=json"
    response = requests.get(url)
    json_data = json.loads(response.text)
    rows = json_data['SchoolSchedule'][1]['row']
    result = {"SC_NM" : rows[0]["SCHUL_NM"], "SC_MTP_NM" : rows[0]["ATPT_OFCDC_SC_NM"], "Events" : []}
    for row in rows:
        result["Events"].append({"Date" : row["AA_YMD"], "Event" : row["EVENT_NM"]})
    return result

def timetable(sc_code, sc_name):
    sd_schul_code = info(sc_code, sc_name)
    result = str("")
    ymd = checkymd()
    url = "https://open.neis.go.kr/hub/misTimetable?KEY=" + key + "&ATPT_OFCDC_SC_CODE=" + sc_code + "&SD_SCHUL_CODE=" + sd_schul_code + "&GRADE=3&CLASS_NM=4&ALL_TI_YMD=" + ymd + "&Type=json"
    response = requests.get(url)
    json_data = json.loads(response.text)
    rows = json_data['misTimetable'][1]['row']
    result = {"SC_NM" : rows[0]["SCHUL_NM"], "SC_MTP_NM" : rows[0]["ATPT_OFCDC_SC_NM"], "Timetables" : []}
    for row in rows:
        result["Timetables"].append({"Date" : row["ALL_TI_YMD"], "Grade" : row["GRADE"], "Class" : row["CLASS_NM"], "Time" : row["PERIO"], "Subject" : row["ITRT_CNTNT"]})
    return result


def meal(sc_code, sc_name):
    sd_schul_code = info(sc_code, sc_name)
    result = []
    now = datetime.datetime.now()
    if now.hour >= 13:
        tomorrow = now + datetime.timedelta(days=1)
        ymd = tomorrow.strftime('%Y%m%d')
    else:
        ymd = now.strftime('%Y%m%d')
    url = "https://open.neis.go.kr/hub/mealServiceDietInfo?KEY=" + key + "&ATPT_OFCDC_SC_CODE=" + sc_code + "&SD_SCHUL_CODE=" + sd_schul_code + "&MLSV_YMD=" + ymd + "&Type=json"
    response = requests.get(url)
    json_data = json.loads(response.text)
    rows = json_data['mealServiceDietInfo'][1]['row']

    allergens = {
        "1.": "난류",
        "2.": "우유",
        "3.": "메밀",
        "4.": "땅콩",
        "5.": "대두",
        "6.": "밀",
        "7.": "고등어",
        "8.": "게",
        "9.": "새우",
        "10.": "돼지고기",
        "11.": "복숭아",
        "12.": "토마토",
        "13.": "아황산류",
        "14.": "호두",
        "15.": "닭고기",
        "16.": "쇠고기",
        "17.": "오징어",
        "18.": "조개류"
    }

    for row in rows:
        menu = row["DDISH_NM"].replace("<br/>", "").replace(" ", "").replace(")", ") ")
        for code, allergen in allergens.items():
            menu = menu.replace(code, allergen + ".")

        meal_info = {
            "식사구분": row["MMEAL_SC_NM"],
            "메뉴": menu,
            "칼로리": row["CAL_INFO"]
        }
        result.append(meal_info)
    return result

if schedule("B10", "서울대학교사범대학부설중학교") != "Internal Server Error":
    if timetable("B10", "서울대학교사범대학부설중학교") != "Internal Server Error":
        if meal("B10", "서울대학교사범대학부설중학교") != "Internal Server Error":
            print("BACK READY")
else:
    exit(1)