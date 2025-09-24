import requests

try:
    from plyer import notification
    plyer_available = True
except ImportError:
    plyer_available = False

city = "Chennai"
geo_url = "https://geocoding-api.open-meteo.com/v1/search"
geo_params = {"name": city, "count": 1, "language": "en", "format": "json"}
geo_response = requests.get(geo_url, params=geo_params).json()

if "results" in geo_response and geo_response["results"]:
    latitude = geo_response["results"][0]["latitude"]
    longitude = geo_response["results"][0]["longitude"]
    print(f"Latitude: {latitude}, Longitude: {longitude}")

    # 2. Get weather data
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation,weathercode",
        "timezone": "auto"
    }
    weather_response = requests.get(weather_url, params=weather_params).json()
    if "current_weather" in weather_response:
        current_weather = weather_response["current_weather"]
        temperature = current_weather["temperature"]
        wind = current_weather["windspeed"]
        weather_code = current_weather["weathercode"]
        weather_info = f"{city}: {temperature}°C, wind {wind} km/h"

        print("weather:", weather_info)

        # 3. Cross-platform notification
        if plyer_available:
            notification.notify(
                title="Weather Update",
                message=weather_info,
                timeout=5
            )
        else:
            print("plyer not installed, skipping notification.")
    else:
        print("Weather data not found")
else:
    print("City not found.")

