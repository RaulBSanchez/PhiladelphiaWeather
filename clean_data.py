import pandas as pd 

df = pd.read_csv('output_dataframe.csv')



# Round all the values to two decimal places
df['temperature_2m_max'] = df['temperature_2m_max'].round(2)
df['temperature_2m_min'] = df['temperature_2m_min'].round(2)
df['apparent_temperature_max'] = df['apparent_temperature_max'].round(2)
df['apparent_temperature_min'] = df['apparent_temperature_min'].round(2)
df['wind_speed_10m_max'] = df['wind_speed_10m_max'].round(2)
df['wind_gusts_10m_max'] = df['wind_gusts_10m_max'].round(2)
df['apparent_temperature_mean'] = df['apparent_temperature_mean'].round(2)
df['temperature_2m_mean'] = df['temperature_2m_mean'].round(2)






df = df.dropna()

# Codes for weather code
# =============================================================================
# clearSky = 0
# mainlyClear = 1
# partlyCloudy = 2
# overcast = 3
# fog = 45
# depositingRimeFog = 48
# lightDrizzle = 51
# moderateDrizzle = 53
# denseDrizzle = 55
# lightFreezingDrizzle = 56
# moderateOrDenseFreezingDrizzle = 57
# lightRain = 61
# moderateRain = 63
# heavyRain = 65
# lightFreezingRain = 66
# moderateOrHeavyFreezingRain = 67
# slightSnowfall = 71
# moderateSnowfall = 73
# heavySnowfall = 75
# snowGrains = 77
# slightRainShowers = 80
# moderateRainShowers = 81
# heavyRainShowers = 82
# slightSnowShowers = 85
# heavySnowShowers = 86
# thunderstormSlightOrModerate = 95
# thunderstormStrong = 96
# thunderstormHeavy = 99
# =============================================================================

df['weather_code'] = df['weather_code'].astype(int)

weather_map_code = {
    0 : "clearSky",
    1 : "mainlyClear",
    2 : "partlyCloudy",
    3 : "overcast",
    45 : "fog",
    48 : "depositingRimeFog",
    51 : "lightDrizzle",
    53 : "moderateDrizzle",
    55 : "denseDrizzle",
    56 : "lightFreezingDrizzle",
    57 : "moderateOrDenseFreezingDrizzle",
    61 : "lightRain",
    63 : "moderateRain",
    65 : "heavyRain",
    66 : "lightFreezingRain",
    67 : "moderateOrHeavyFreezingRain",
    71 : "slightSnowfall",
    73 : "moderateSnowfall",
    75 : "heavySnowfall",
    77 : "snowGrains",
    80 : "slightRainShowers",
    81 : "moderateRainShowers",
    82 : "heavyRainShowers",
    85 : "slightSnowShowers",
    86 : "heavySnowShowers",
    95 : "thunderstormSlightOrModerate",
    96 : "thunderstormStrong",
    99 : "thunderstormHeavy"

}



# Map the weather codes 
df['weather_code'] = df['weather_code'].map(weather_map_code)

def compassConvert(degree):
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    index = int((degree + 22.5) % 360 / 45)
    return directions[index]

df['wind_direction'] = df['wind_direction_10m_dominant'].apply(compassConvert)



#Remove the time and only return the date
df['date'] = pd.to_datetime(df['date']).dt.date



#Convert the sunrise/sunset times in epoch time to readable data
df['sunriseTime'] = pd.to_datetime(df['sunrise'], unit='s')
df['sunriseTime'] = df['sunriseTime'] - pd.Timedelta(hours=4)
df['sunsetTime'] = pd.to_datetime(df['sunset'], unit='s')
df['sunsetTime'] = df['sunsetTime'] - pd.Timedelta(hours=4)
print(df.dtypes)

#Place all the months into Seasonal Categories
def season(date):
    month = date.month
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3,4,5]:
        return 'Spring'
    elif month in [6,7,8]:
        return 'Summer'
    else:
        return 'Fall'
    
df['season'] = df['date'].apply(season)

#Export the clean data for analysis
df.to_csv('CleanData.csv', index=False) 