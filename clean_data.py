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



print(df.isna().sum())


df = df.dropna()

print(df.isna().sum())