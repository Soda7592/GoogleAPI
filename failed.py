import requests as req
from geopy.geocoders import Nominatim
from math import hypot
import random
import json
import tkinter as tk

APPname = ["MyAPP", "MyAPP1", "MyAPP2", "MyAPP3", "MyAPP4", "MyAPP5"]
geolocator = Nominatim(user_agent=random.choice(APPname))
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
                print(x1, y1)
                dis = hypot(float(x1) - float(x2), float(y1) - float(y2))
                if dis < min:
                    min = dis
                    index = i
            print(locat[index])
            return locat[index]


def SearchPM25(Site):
    # print(Site)
    url = "https://data.epa.gov.tw/api/v2/aqx_p_488?format=json&offset=0&limit=5&api_key=< api key  >&filters=SiteName,EQ,"
    res = req.get(url + Site)
    data = json.loads(res.content)
    return [
        data["records"][0]["pm2.5"],
        data["records"][0]["status"],
        data["records"][0]["county"],
    ]


def buttonGet():
    place = place_info.get()
    if place != "":
        entry_place = tk.Entry(window, textvariable=place_info)
        entry_place.grid(row=0, column=1)
        location = geolocator.geocode(place)
        # print(place)
        x1 = location.latitude
        y1 = location.longitude
        nearest = SearchShortestSite(x1, y1).strip("\n")
        data = SearchPM25(nearest)
        station = f"最近的測站是 :{data[2]}{nearest}測站"
        air_status = f"PM2.5 濃度是: {data[0]}\n 空氣品質狀況 : {data[1]}"
        label_air = tk.Label(window, text=air_status)
        label_air.grid(row=1, column=0)
        label_station = tk.Label(window, text=station)
        label_station.grid(row=2, column=0)
    # return air_status, label_station


window = tk.Tk()
window.title("空氣檢測")
window.geometry("500x500")
window.resizable(True, True)
place_info = tk.StringVar()
label_place = tk.Label(window, text="請輸入當前位置")
label_place.grid(row=0, column=0)
entry_place = tk.Entry(window, textvariable=place_info)
entry_place.grid(row=0, column=1)
button = tk.Button(window, text="確認", command=buttonGet)
button.grid(row=2, column=0)


if __name__ == "__main__":

    place_info = tk.StringVar()
    label_place = tk.Label(window, text="請輸入當前位置")
    label_place.grid(row=0, column=0)
    entry_place = tk.Entry(window, textvariable=place_info)
    entry_place.grid(row=0, column=1)
    button = tk.Button(window, text="確認", command=buttonGet)
    button.grid(row=2, column=0)
    window.update()
    window.mainloop()
