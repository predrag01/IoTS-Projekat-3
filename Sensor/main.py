import os
from datetime import datetime

import psycopg2
import argparse
import time
import paho.mqtt.publish as publish
import json

topic = "sensor/weather-data"

def test_connection():
    try:
        connection = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="1234",
            host="postgres",
            port="5432",
        )
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(f"Connected to database: {db_version}")

        cursor.close()
        connection.close()

    except Exception as error:
        print("Error while connecting to PostgreSQL", error)

def get_ids():
    try:
        connection = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="1234",
            host="postgres",
            port="5432",
        )
        cursor = connection.cursor()

        sql = """SELECT DISTINCT("measurementid") FROM "weatherdata" """
        cursor.execute(sql)
        records = cursor.fetchall()

        cursor.close()
        connection.close()

        measurement_ids = []
        for row in records:
            #print(row)
            measurement_ids.append(row[0])

        return measurement_ids

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
        return 0

def start_reading(measurement_ids, sleep):
    try:
        connection = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="1234",
            host="postgres",
            port="5432",
        )
        cursor = connection.cursor()

        sql = """SELECT * FROM "weatherdata" WHERE "measurementid" = %s """

        for id in measurement_ids:
            cursor.execute(sql, (id,))
            records = cursor.fetchone()

            if records is None:
                print(f"No records found for MeasurementId: {id}")
                continue

            data = {
                "StationName": records[0],
                "MeasurementTimestamp": records[1].isoformat() if isinstance(records[1], datetime) else records[1],
                "AirTemperature": float(records[2]) if records[2] is not None else None,
                "WetBulbTemperature": float(records[3]) if records[3] is not None else None,
                "Humidity": int(records[4]) if records[4] is not None else None,
                "RainIntensity": float(records[5]) if records[5] is not None else None,
                "IntervalRain": float(records[6]) if records[6] is not None else None,
                "TotalRain": float(records[7]) if records[7] is not None else None,
                "PrecipitationType": int(records[8]) if records[8] is not None else None,
                "WindDirection": float(records[9]) if records[9] is not None else None,
                "WindSpeed": float(records[10]) if records[10] is not None else None,
                "MaximumWindSpeed": float(records[11]) if records[11] is not None else None,
                "BiometricPressure": float(records[12]) if records[12] is not None else None,
                "SolarRadiation": int(records[13]) if records[13] is not None else None,
                "Heading": int(records[14]) if records[14] is not None else None,
                "BatteryLife": records[15],
                "MeasurementTimestampLabel": records[16],
                "MeasurementId": records[17]
            }
            json_data = json.dumps(data)
            print(json_data)

            try:
                publish.single(
                    topic + "/" + str(id),
                    payload=json_data,
                    hostname="mosquitto",
                    port=8883,
                    client_id="",
                    keepalive=60,
                    qos=0,
                    retain=False,
                )
            except Exception as e:
                print("Error while publishing message", e)

            time.sleep(sleep)

        cursor.close()
        connection.close()

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
        return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process weather data.')
    parser.add_argument('--sleep', type=int, default=3, help='Sleep time between processing batches')

    args = parser.parse_args()
    sleep = args.sleep

    test_connection()
    measurement_ids = get_ids()
    start_reading(measurement_ids, sleep)
