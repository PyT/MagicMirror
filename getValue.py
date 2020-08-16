import Adafruit_DHT
import requests
import json
import datetime

def pushToLaMetric(value,value2,valueList):
    url = "https://developer.lametric.com/api/V1/dev/widget/update/com.lametric.7401034921a3efbac52ba06c6e5a1734/3"
    payload = {"frames":[{"text":"25°", "icon":"i2056","index":0},{"text":"x%","icon":"a2423","index":1},{"index":2,"chartData":[]}]}
    payload["frames"][0]["text"]=str(value)+"°"
    payload["frames"][1]["text"]=str(value2)+"%"
    payload["frames"][2]["chartData"]=valueList
    headers = {"Accept":"application/json","X-Access-Token":"N2IwMjEyNGMyNGMzY2I3MTViZWMxOTU0YzliZmJiMTY3MzQ4YTJhYWNmZGY1NTc2NTA0YWFkMGIwODViNzQ2Ng==","Cache-control":"no-cache"}
    print(payload)
    r = requests.post(url,data=json.dumps(payload),headers=headers)

def extract_date(json):
    try:
        if len(str(json["hour"]))==1:
           h = "0"+str(json["hour"])
        else:
           h = str(json["hour"])
        return int(str(json["date"])+h)
    except Exception as e:
        print("error {}".format(e))
        return 0

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
humidity,temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

f = open("values.txt","r+")
file_content = f.read().rstrip()
dic = json.loads(file_content)
previous_values=[]

dic.sort(key=extract_date)

hour = datetime.datetime.now().hour
print(hour)
date = datetime.datetime.now().strftime("%Y%m%d")
print(date)

temp_100 = int(temperature*10)


for item in dic:
   current_hour = item["hour"]
   if current_hour == hour and date != item["date"]:
      print("Replace {}".format(hour))
      item["value"]=temp_100
      item["date"]=date

dic.sort(key=extract_date)

for item in dic:
    v = item["value"]
    previous_values.append(v)

print(dic)
m = min(previous_values)

previous_values = [item - m for item in previous_values]
previous_values = [int(item) for item in previous_values]

print(previous_values)
f.seek(0)

json.dump(dic,f)
f.close()


if humidity is not None and temperature is not None:
	print("Temp={0:0.1f}*C Humidity={1:0.1f}".format(temperature,humidity))
	pushToLaMetric(round(temperature,1),round(humidity,1),previous_values)

