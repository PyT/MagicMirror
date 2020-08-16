import requests
import json
import datetime

def getValuesFromMeteoFrance():
    url="http://webservice.meteofrance.com/rain?lang=fr&lat=48.8713863&lon=2.3571334&token=__Wj7dVSTjV9YGu1guveLyDq0g7S7TfTjaHBTPTpO0kj8__"
    r = requests.get(url)
    t=r.text
    j=json.loads(t)
    print(j)
    result=[]
    for item in j["forecast"]:
        if item["rain"]>=2:
            #print("RAIN")
            d = datetime.datetime.fromtimestamp(int(item["dt"]))
            d_str = d.strftime("%H:%M")
            result.append(d_str)
        #else:
            #print("NO RAIN")
            #d = datetime.datetime.fromtimestamp(int(item["dt"]))
            #d_str=d.strftime("%H:%M")
            #result.append(d_str)
    return result


def pushToLaMetric(value,icon):
    url = "https://developer.lametric.com/api/V1/dev/widget/update/com.lametric.d4e3b2b209320a7ede8f8d491f7b1b9b/3"
    payload = {"frames":[{"text":"25°", "icon":"a72","index":0}]}
    payload["frames"][0]["text"]=str(value)
    payload["frames"][0]["icon"]=icon
    headers = {"Accept":"application/json","X-Access-Token":"N2IwMjEyNGMyNGMzY2I3MTViZWMxOTU0YzliZmJiMTY3MzQ4YTJhYWNmZGY1NTc2NTA0YWFkMGIwODViNzQ2Ng==","Cache-control":"no-cache"}
    print(payload)
    r = requests.post(url,data=json.dumps(payload),headers=headers)


r=getValuesFromMeteoFrance()
if len(r)>0:
    buff = " ".join(r)
    i = "a72"
    v = "Pluie prevue ({})".format(buff)
else:
    i = "a1246"
    v = "Pas de pluie"

pushToLaMetric(v,i)
