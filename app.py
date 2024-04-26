from flask import Flask, render_template, request
import requests as req
from geopy.geocoders import Nominatim
from math import hypot
from fake_useragent import UserAgent
import json


app = Flask(__name__)
user_agent = UserAgent()
geolocator = Nominatim(user_agent=user_agent.random)
PMprotect = open("protect.txt", "r", encoding="utf-8").readlines()
# print(PMprotect[0])
index = 0
x1 = 0
y1 = 0


def SearchShortestSite(x1, y1):
    with open("lnglat.txt", "r") as f:
        with open("location.txt", "r", encoding="utf-8") as fw:
            locat = fw.readlines()
            l = f.readlines()
            min = 99999999999
            for i in range(len(l)):
                point = l[i][0:-2].split(",")
                x2 = point[0]
                y2 = point[1]
                # print(x1, y1)
                dis = hypot(float(x1) - float(x2), float(y1) - float(y2))
                if dis < min:
                    min = dis
                    index = i
            # print(locat[index])
            return locat[index]


def SearchPM25(Site):
    # print(Site)
    url = "https://data.epa.gov.tw/api/v2/aqx_p_488?format=json&offset=0&limit=5&api_key=< api key >&filters=SiteName,EQ,"
    res = req.get(url + Site)
    data = json.loads(res.content)
    return data["records"][0]
    # return [
    #     data["records"][0]["pm2.5"],
    #     data["records"][0]["status"],
    #     data["records"][0]["county"],
    # ]


def PM2_level(level):
    if level >= 0 and level <= 35:
        return 0
    elif level >= 36 and level <= 53:
        return 1
    elif level >= 54 and level <= 70:
        return 2
    elif level >= 71:
        return 3


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/air")
def air():
    name = request.args.get("nameis")
    location = geolocator.geocode(name)
    x1 = location.latitude
    y1 = location.longitude
    nearest = SearchShortestSite(x1, y1).strip("\n")
    data = SearchPM25(nearest)
    level = int(PM2_level(int(data["pm2.5"])))  # PMprotect[int(data["pm2.5"])]
    measure = PMprotect[level].split("。")
    # print(level)
    # print(PMprotect[level])
    return render_template("page.html", namepage=data, protect=measure)


if __name__ == "__main__":
    app.run(debug=True)
