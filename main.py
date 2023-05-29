import requests
import json

keyfile = open('key.txt', 'r')
key = keyfile.read()
print(key)
keyfile.close()

def schedule():
    url = "https://open.neis.go.kr/hub/SchoolSchedule?KEY=" + key + "&ATPT_OFCDC_SC_CODE=D10&SD_SCHUL_CODE=7261025&AA_YMD=202305&Type=json"
    response = requests.get(url)
    json_data = json.loads(response.te5xt)
    print(json_data)

schedule()