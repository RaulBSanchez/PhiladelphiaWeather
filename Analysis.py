#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 20 13:45:54 2025

@author: raulbazan
"""

import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv('CleanData.csv')
print(df.dtypes)
df["date"] = pd.to_datetime(df["date"])
df["year"] = df["date"].dt.year
print("new types")
print(df.dtypes)

seasonal_temp = df.groupby(["year","season"] )["temperature_2m_max"].mean().reset_index()
seasonal_temp = seasonal_temp.sort_values(["season", "year"])
seasonal_temp["pct_change"] = seasonal_temp.groupby("season")["temperature_2m_max"].pct_change() * 100

print('seasonal temp')
print(seasonal_temp.dtypes)



print(seasonal_temp)

#FeelsLikeTemp = df.groupby(["year","season"])["apparent_temperature_mean"].mean().reset_index()
maxTemp = df.groupby(["year", "season"])["temperature_2m_max"].mean().reset_index()

# 3. Plot
# pivot_df = maxTemp.pivot(index="year", columns="season", values="temperature_2m_max")

# # Plot
# pivot_df.plot(marker='o', figsize=(10, 6))
# plt.title("Seasonal Apparent Temperature Trends Over Years")
# plt.xlabel("Year")
# plt.ylabel("Avg Apparent Temperature (°F)")
# plt.grid(True)
# plt.legend(title="Season")
# plt.tight_layout()
# plt.show()


seasonal = seasonal_temp.pivot(index="year", columns="season", values="pct_change")

seasonal.plot(kind='bar', figsize=(10,6))
plt.title("Percentage Change in Average Max Temps")
plt.xlabel("Year")
plt.ylabel("Percentage change")
plt.grid(True)
plt.legend(title="Season")
plt.tight_layout()
plt.show()