from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SensorData
from datetime import datetime, timedelta, timezone
from django.db.models import Avg
import joblib
import pandas as pd
import random
import numpy as np

def index(request):
    return HttpResponse("Hello, you are at backend server")



def getAverageValues():
    # Calculate time ranges day=1, week=2, month=??(impliment if required),year=??(impliment if required)
    #filtering records based on time
    end_date = datetime.now(timezone.utc) #end_date is current timestamp
    start_date_1_day = end_date - timedelta(days=1) # minus the 1 day from current timestamp
    start_date_1_week = end_date - timedelta(weeks=1) # minus the 1 week from current timestamp

    # Get sensor data for the last 1 day and calculate averages
    data_1_day = SensorData.objects.filter(timestamp__gte=start_date_1_day, timestamp__lte=end_date)
    # print("////-")
    # # print(data_1_day)
    # print("///")
    # read data from data_day_1(returns record for last one day) object and apply AVG on dictonary key(temperature) and aggrigate it and store in alias avg_temprature
    average_temperature_1_day = data_1_day.aggregate(avg_temperature=Avg('temperature'))['avg_temperature']
    average_humidity_1_day = data_1_day.aggregate(avg_humidity=Avg('humidity'))['avg_humidity']
    average_moisture_1_day = data_1_day.aggregate(avg_moisture=Avg('moisture'))['avg_moisture']
    average_lux_1_day = data_1_day.aggregate(avg_lux=Avg('lux'))['avg_lux']
    average_pH_1_day = data_1_day.aggregate(avg_pH=Avg('phlevel'))['avg_pH']

    # Get sensor data for the last 1 week and calculate averages
    data_1_week = SensorData.objects.filter(timestamp__gte=start_date_1_week, timestamp__lte=end_date)
    average_temperature_1_week = data_1_week.aggregate(avg_temperature=Avg('temperature'))['avg_temperature']
    average_humidity_1_week = data_1_week.aggregate(avg_humidity=Avg('humidity'))['avg_humidity']
    average_moisture_1_week = data_1_week.aggregate(avg_moisture=Avg('moisture'))['avg_moisture']
    average_lux_1_week = data_1_week.aggregate(avg_lux=Avg('lux'))['avg_lux']
    average_pH_1_week = data_1_week.aggregate(avg_pH=Avg('phlevel'))['avg_pH']

    # print("Last 1 day:")
    # print(f"Average Temperature: {average_temperature_1_day:.2f}")
    # print(f"Average Humidity: {average_humidity_1_day:.2f}")

    # print("\nLast 1 week:")
    # print(f"Average Temperature: {average_temperature_1_week:.2f}")
    # print(f"Average Humidity: {average_humidity_1_week:.2f}")
    
    avg_details = {
        "last_1_day":{
            "temperature": round(average_temperature_1_day,2),
            "humidity":round(average_humidity_1_day,2),
            "moisture":round(average_moisture_1_day,2),
            "lux":round(average_lux_1_day,2),
            "pH":round(average_pH_1_day,2),
        },
        "last_1_week":{
            "temperature":round(average_temperature_1_week,2),
            "humidity":round( average_humidity_1_week,2),
            "moisture":round(average_moisture_1_week,2),
            "lux":round(average_lux_1_week,2),
            "pH":round(average_pH_1_week,2),
        }
    }
    return avg_details

class latestSensorData(APIView):
    def get(self, request, format=None):

        #get latest sensor data       
      
        obj = SensorData.objects.latest('timestamp') #latest one row from mysql
        # print(obj)
        # print(obj.timestamp)
        # print(obj.id)
        # print(obj.temperature)
        # print(obj.humidity)

        #get average of data for week, day
        all_avg_values = getAverageValues()

        formatted_timestamp = obj.timestamp.strftime('%A, %B %d, %Y - %I:%M %p') #fromated timestap in human readable format

        result = {
            "latest":{
                "temperature": obj.temperature,
                "humidity": obj.humidity,
                "moisture":obj.moisture,
                "lux":obj.lux,
                "pH":obj.phlevel,
                "timestamp":formatted_timestamp#obj.timestamp
            },
            "average": all_avg_values
        }

        return Response(result) # send result dictonary to angular
    

    # def post(self, request, format=None):
        
    #     return Response("HELLO POST")



class liveRecordsSensorData(APIView):
    def get(self, request, format=None):
        last_minutes = 10 # no of record avg in last 10 minutes

        # Calculate the time range for the last 10 minutes   #same as above 1 day 1 week but for minutes
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(minutes=last_minutes)        

        # Query sensor data for the last 10 minutes
        data_last_10_minutes = SensorData.objects.filter(timestamp__gte=start_time, timestamp__lte=end_time)

        # Group data by minute intervals and calculate average temperature and humidity for each minute
        data_per_minute = (
            data_last_10_minutes
            .extra(
                select={'minute': "DATE_FORMAT(timestamp, '%%Y-%%m-%%d %%H:%%i:00')"}
            )
            .values('minute')
            .annotate(avg_temperature=Avg('temperature'), avg_humidity=Avg('humidity'), avg_moisture=Avg('moisture'), avg_lux=Avg('lux'),avg_pH=Avg('phlevel'))
        )

        # Create a dictionary to store the average values for each minute
        minute_data = {entry['minute']: {
            'temperature': round(entry['avg_temperature'], 2), 
            'humidity': round(entry['avg_humidity'], 2), 
            'moisture': round(entry['avg_moisture'], 2), 
            'lux': round(entry['avg_lux'], 2),
            'pH': round(entry['avg_pH'], 2)
            } for entry in data_per_minute}

        # Create a list of all possible minute intervals within the time range
        all_minutes = [(start_time + timedelta(minutes=i)).strftime('%Y-%m-%d %H:%M:00') for i in range(0, last_minutes+1)]

        # Initialize the list of live records
        live_records = []

        # Iterate through all possible minute intervals and populate live records
        for minute in all_minutes:
            record = {
                'minute': minute,
                'temperature': minute_data.get(minute, {'temperature': 0})['temperature'],
                'humidity': minute_data.get(minute, {'humidity': 0})['humidity'],
                'moisture': minute_data.get(minute, {'moisture': 0})['moisture'],
                'lux': minute_data.get(minute, {'lux': 0})['lux'],
                'pH': minute_data.get(minute, {'pH': 0})['pH'],
            }
            live_records.append(record)

        print("live data length: ")
        print(len(live_records))
        result = {
            'liveRecords': live_records
        }

        return Response(result)
    

    # def post(self, request, format=None):
        
    #     return Response("HELLO POST")
    

#for prediction

class CropPredictionAPI(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Retrieve data from the database (you can modify this based on your database structure)
        
            obj = SensorData.objects.latest('timestamp') #latest one row from mysql
        
            temperature = obj.temperature
            humidity = obj.humidity
            moisture = obj.moisture
            ph = obj.phlevel
            light_intensity = obj.lux

            # Load the trained models from the .pkl files
            yield_model = joblib.load('yield_model.pkl')
            health_model = joblib.load('health_classifier.pkl')

            # Predict crop yield using the yield model
            yield_prediction = yield_model.predict([[temperature, humidity, moisture, ph, light_intensity]])

            # Predict crop health using the health model
            health_prediction = health_model.predict([[temperature, humidity, moisture, ph, light_intensity]])

            # Map numerical health prediction to human-readable labels
            health_labels = {0: 'Very Poor', 1: 'Poor', 2: 'Fair', 3: 'Good', 4: 'Excellent'}
            health_prediction_label = health_labels[int(health_prediction[0])]


            result = {
                'predicted_yield': round(yield_prediction[0],2), 
                'predicted_health': health_prediction_label
            }

            return Response(result)
        
        except Exception as e:
            return Response({'error': str(e)})