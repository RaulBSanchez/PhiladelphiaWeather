import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
	"latitude": 39.9524,
	"longitude": -75.1636,
	"start_date": "1995-07-15",
	"end_date": "2025-07-16",
	"daily": ["temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant", "sunrise", "sunset", "precipitation_sum", "rain_sum", "snowfall_sum", "weather_code", "apparent_temperature_mean", "temperature_2m_mean"],
	"timezone": "America/New_York",
	"temperature_unit": "fahrenheit",
	"wind_speed_unit": "mph"
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
daily_apparent_temperature_max = daily.Variables(2).ValuesAsNumpy()
daily_apparent_temperature_min = daily.Variables(3).ValuesAsNumpy()
daily_wind_speed_10m_max = daily.Variables(4).ValuesAsNumpy()
daily_wind_gusts_10m_max = daily.Variables(5).ValuesAsNumpy()
daily_wind_direction_10m_dominant = daily.Variables(6).ValuesAsNumpy()
daily_sunrise = daily.Variables(7).ValuesInt64AsNumpy()
daily_sunset = daily.Variables(8).ValuesInt64AsNumpy()
daily_precipitation_sum = daily.Variables(9).ValuesAsNumpy()
daily_rain_sum = daily.Variables(10).ValuesAsNumpy()
daily_snowfall_sum = daily.Variables(11).ValuesAsNumpy()
daily_weather_code = daily.Variables(12).ValuesAsNumpy()
daily_apparent_temperature_mean = daily.Variables(13).ValuesAsNumpy()
daily_temperature_2m_mean = daily.Variables(14).ValuesAsNumpy()

daily_data = {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}

daily_data["temperature_2m_max"] = daily_temperature_2m_max
daily_data["temperature_2m_min"] = daily_temperature_2m_min
daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
daily_data["apparent_temperature_min"] = daily_apparent_temperature_min
daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max
daily_data["wind_direction_10m_dominant"] = daily_wind_direction_10m_dominant
daily_data["sunrise"] = daily_sunrise
daily_data["sunset"] = daily_sunset
daily_data["precipitation_sum"] = daily_precipitation_sum
daily_data["rain_sum"] = daily_rain_sum
daily_data["snowfall_sum"] = daily_snowfall_sum
daily_data["weather_code"] = daily_weather_code
daily_data["apparent_temperature_mean"] = daily_apparent_temperature_mean
daily_data["temperature_2m_mean"] = daily_temperature_2m_mean

daily_dataframe = pd.DataFrame(data = daily_data)
#print(daily_dataframe.)

daily_dataframe.to_csv('output_dataframe.csv', index=False)