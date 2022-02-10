from fastapi import FastAPI

import json
import pandas as pd
from datetime import datetime


def timestamp_to_date(timestamp):
    dt_obj = datetime.fromtimestamp(int(str(timestamp)[0:10]))
    print(timestamp)
    print(dt_obj.strftime("%d-%m"))
    return dt_obj.strftime("%d-%m")


# Grab Salary data from JSON file
f = open("sensor_data.json")
array = json.load(f)
data = array.get("array")
f.close()

pd.set_option('display.max_rows', None)
df = pd.json_normalize(data)
df_day = df['timestamp'].apply(timestamp_to_date)
df['date'] = df_day
df_groupby_room = df.groupby('roomArea')
df_groupby_day = df.groupby('date')

app = FastAPI()


@app.get("/")
async def root():
    return array


@app.get("/date/{month}/{date}")
async def get_by_date(month: str, date: str):
    df_return = df_groupby_day.get_group(f"{date}-{month}")
    result = df_return.to_json(orient="records", indent=4)
    return json.loads(result)


# 07/02 -> 07/12
@app.get("/date/{month}/{date}/stats")
async def get_by_date_stats(month: str, date: str):
    df_return = df_groupby_day.get_group(f"{date}-{month}")

    temp = df_return['temperature']
    hum = df_return['humidity']

    minTemp = temp.min()
    maxTemp = temp.max()
    medianTemp = temp.median()
    avgTemp = temp.mean()

    minHum = hum.min()
    maxHum = hum.max()
    medianHum = hum.median()
    avgHum = hum.mean()

    stats = [['Minimum Temperature', minTemp],
             ['Maximum Temperature', maxTemp],
             ['Median Temperature', medianTemp],
             ['Average Temperature', avgTemp],
             ['Minimum Humidity', minHum],
             ['Maximum Humidity', maxHum],
             ['Median Temperature', medianHum],
             ['Average Temperature', avgHum]]
    df_final = pd.DataFrame(stats, columns=['Info', 'Value'])
    df_json = df_final.to_json(orient="records", indent=4)

    return json.loads(df_json)


@app.get("/room/{num}")
async def get_by_room(num: str):
    df_return = df_groupby_room.get_group(f"roomArea{num}")
    result = df_return.to_json(orient="records", indent=4)
    return json.loads(result)


@app.get("/room/{num}/stats")
async def get_by_room_stats(num: str):
    df_return = df_groupby_room.get_group(f"roomArea{num}")

    temp = df_return['temperature']
    hum = df_return['humidity']

    minTemp = temp.min()
    maxTemp = temp.max()
    medianTemp = temp.median()
    avgTemp = temp.mean()

    minHum = hum.min()
    maxHum = hum.max()
    medianHum = hum.median()
    avgHum = hum.mean()

    stats = [['Minimum Temperature', minTemp],
             ['Maximum Temperature', maxTemp],
             ['Median Temperature', medianTemp],
             ['Average Temperature', avgTemp],
             ['Minimum Humidity', minHum],
             ['Maximum Humidity', maxHum],
             ['Median Temperature', medianHum],
             ['Average Temperature', avgHum]]
    df_final = pd.DataFrame(stats, columns=['Info', 'Value'])
    df_json = df_final.to_json(orient="records", indent=4)

    return json.loads(df_json)
