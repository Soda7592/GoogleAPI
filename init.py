import requests as req
import json
import urllib3
import datetime

urllib3.disable_warnings()

print("begin time: ", datetime.datetime.now())

county = [
    "高雄市",
    "雲林縣",
    "金門縣",
    "連江縣",
    "苗栗縣",
    "花蓮縣",
    "臺東縣",
    "臺南市",
    "臺北市",
    "臺中市",
    "澎湖縣",
    "桃園市",
    "新竹縣",
    "新竹市",
    "新北市",
    "彰化縣",
    "屏東縣",
    "宜蘭縣",
    "基隆市",
    "嘉義縣",
    "嘉義市",
    "南投縣",
]

l = []
with open("lnglat.txt", "w") as f:
    with open("location.txt", "w", encoding="utf-8") as fw:
        for i in county:
            url = "https://data.epa.gov.tw/api/v2/aqx_p_488?format=json&offset=0&limit=5&api_key=< api key  >&filters=county,EQ,"
            res = req.get(url + i)
            data = json.loads(res.content)
            for j in data["records"]:
                s = str(j["sitename"])
                lnglat = str(j["latitude"] + "," + j["longitude"])
                if s not in l:
                    l.append(s)
                    print(s, lnglat)
                    f.write(lnglat + "\n")
                    fw.write(s + "\n")
