from fastapi import FastAPI

import json
import pandas as pd
from datetime import datetime


def timestamp_to_date(timestamp):
    dt_obj = datetime.fromtimestamp(int(str(timestamp)[0:10]))
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
async def say_hello(month: str, date: str):
    df_return = df_groupby_day.get_group(f"{date}-{month}")
    result = df_return.to_json(orient="records", indent=4)
    return json.loads(result)


@app.get("/room/{num}")
async def say_hello(num: str):
    df_return = df_groupby_room.get_group(f"roomArea{num}")
    result = df_return.to_json(orient="records", indent=4)
    return json.loads(result)


@app.get("/room/{num}/stats")
async def say_hello(num: str):
    df_return = df_groupby_room.get_group(f"roomArea{num}")
    minTemp = df_return['temperature'].min()
    maxTemp = df_return['temperature'].max()
    medianTemp = df_return['temperature'].median()
    avgTemp = df_return['temperature'].mean()

    minHum = df_return['Humidity'].min()
    maxHum = df_return['Humidity'].max()
    medianHum = df_return['Humidity'].median()
    avgHum = df_return['Humidity'].mean()

    return minTemp
