
import tokens
import os
from datetime import datetime, timedelta
str_to_date = lambda s: datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%fZ')
date_to_str = lambda d: d.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

def get_timestamps(init_time: datetime, final_time: datetime, step_duration: timedelta) -> list[datetime]:
    timestamps = []
    t = init_time
    while t <= final_time:
        timestamps.append(t)
        t += step_duration
    return timestamps

import numpy as np
# REF: https://www.weather.gov/media/epz/wxcalc/vaporPressure.pdf
# REF: https://web.archive.org/web/20200212215746im_/https://www.vaisala.com/en/system/files?file=documents/Humidity_Conversion_Formulas_B210973EN.pdf
vapor_pressure = lambda T: 10**(7.5*T/(237.3+T)) # 6.11 *
relative_humidity = lambda T, T_d: 100 * vapor_pressure(T_d) / vapor_pressure(T) 
# REF: https://journals.ametsoc.org/view/journals/apme/50/11/jamc-d-11-0143.1.xml
wetbulb_temperature = lambda T, RH: T * np.arctan(0.151977 * (RH + 8.313659)**0.5) + np.arctan(T + RH) - np.arctan(RH - 1.676331) + 0.00391838 * (RH)**(3/2) * np.arctan(0.023101 * RH) - 4.686035
C2F = lambda num: (num*9/5)+32 # celsius_to_farhenheit
wue = lambda cycle, tw: max(.0,cycle/(cycle-1)*(6e-5* C2F(tw)**3 - 0.01 * C2F(tw)**2 + 0.61 * C2F(tw) - 10.4))


import csv
import json, sys
def get_weather(city: str, date1: str, date2: str, path: str, include = "hours") -> dict:
    import urllib.request
    """
    API documentation: https://www.visualcrossing.com/resources/documentation/weather-api/timeline-weather-api/
    Metric units:
    Weather Variable                        Measurement Unit
    Temperature, Heat Index & Wind Chill	Degrees Celcius
    Precipitation	                        Millimeters
    Snow	                                Centimeters
    Wind & Wind Gust	                    Kilometers Per Hour
    Visibility	                            Kilometers
    Pressure	                            Millibars (Hectopascals)
    Solar Radiation	                        W/m2
    Solar Energy	                        MJ/m2
    Soil Moisture	                        Millimeters
    """   
    city = city.replace(" ", "%20")  
    format = "json"
    query = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{date1}/{date2}?unitGroup=metric&include={include}&key={tokens.VISUALCROSSING_API_TOKEN}&contentType={format}&timezone=Z"
    #print(query)
    if os.path.isfile(f'{path}{city}_weather.json'):
        return load(path, city)
    # else
    try:
        #sys.exit() 
        ResultBytes = urllib.request.urlopen(query)
        dt = json.load(ResultBytes)
        # Parse the results as CSV
        #CSVText = csv.reader(codecs.iterdecode(ResultBytes, 'utf-8'))
        with open(f'{path}{city}_weather.json', 'w', newline='') as f:
            f.write(json.dumps(dt))
            
    except urllib.error.HTTPError  as e:
        ErrorInfo= e.read().decode() 
        print('Error code: ', e.code, ErrorInfo)
        sys.exit()
    except  urllib.error.URLError as e:
        ErrorInfo= e.read().decode() 
        print('Error code: ', e.code,ErrorInfo)
        sys.exit()
    
    return dt["days"]  

def load(path, city):
    city = city.replace(" ", "%20")
    with open(f'{path}{city}_weather.json', 'r') as f:
        data = json.load(f)
    return data["days"]
    

def wetbulb_temperature_processing(
        city, 
        date_time_start = str_to_date("2023-01-01T00:00:00.000Z"), 
        date_time_finish = str_to_date("2023-12-31T23:00:00.000Z"),
        path = "data_preprocessing",
        include = "hours"
        ):
    date_start = str(date_time_start.date())
    date_finish = str(date_time_finish.date())
    
    data = get_weather(city, date_start, date_finish, path = f"{path}/{date_to_str(date_time_start)}-{date_to_str(date_time_finish)}/", include = include)
    #data = load(f"{path}/{date_to_str(date_time_start)}-{date_to_str(date_time_finish)}/", city)
    wetbulb_temperature_dict = {}
    for day in data:
        day_str = day["datetime"]
        for hour in day["hours"]:
            hour_str = hour["datetime"]
            date_time = datetime.strptime(f'{day_str}T{hour_str}', '%Y-%m-%dT%H:%M:%S')
            if date_time < date_time_start or date_time > date_time_finish:
                continue
            #print(date_to_str(date_time))
            wetbulb_temperature_dict[date_time] = wetbulb_temperature(float(hour["temp"]), relative_humidity(float(hour["temp"]), float(hour["dew"])))
    return wetbulb_temperature_dict