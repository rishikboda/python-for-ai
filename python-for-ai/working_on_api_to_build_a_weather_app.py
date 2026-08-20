import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

city = input("enter the location of the city")
state = input("enter the location of the state")

geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
geo_response = requests.get(geo_url).json()

lat = geo_response["results"][0]["latitude"]
lon = geo_response["results"][0]["longitude"]
print(f"{city} → lat: {lat}, lon: {lon}")

today = datetime.today()
week_ago = today - timedelta(days=7)
start_date = week_ago.strftime("%Y-%m-%d")
end_date = today.strftime("%Y-%m-%d")

weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min"
weather_response = requests.get(weather_url).json()
print(weather_response)
# -------------------------------------------------
daily_data = weather_response["daily"]
df = pd.DataFrame(
    {
        "date": daily_data["time"],
        "max_temp": daily_data["temperature_2m_max"],
        "min_temp": daily_data["temperature_2m_min"],
    }
)

print(df)
df["avg_temp"] = (df["max_temp"] + df["min_temp"]) / 2
# ---------------------------------------------
plt.figure(figsize=(10, 6))
plt.plot(df["date"], df["max_temp"], marker="o", label="max Temp")
plt.plot(df["date"], df["min_temp"], marker="o", label="Min Temp")
plt.plot(df["date"], df["avg_temp"], marker="o", label="avg temp")
plt.xlabel("date")
plt.ylabel("temperature~in c")
plt.title(f"weather report of {city} past 10 days")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("weather report.png")
plt.show()
# -----------------------------
if not os.path.exists("data"):
    os.makedirs("data")

# Save to CSV
df.to_csv("data/paris_weather.csv", index=False)
print("Data saved to data/paris_weather.csv")
