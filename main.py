import datetime
import requests
import re
import json
import os


class WeatherForecast:
    def __init__(self, filename='weather_data.json'):
        self.filename = filename
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        return {}

    def _save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=2)

    def __setitem__(self, date, value):
        self.data[date] = value
        self._save()

    def __getitem__(self, date):
        return self.data[date]

    def __iter__(self):
        return iter(self.data)

    def items(self):
        # Generator yielding (date, weather) tuples
        for date in self.data:
            yield (date, self.data[date])


def get_lat_long(place):
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept-Language': 'en-US,en;q=0.9'
    }

    if place:
        place_encoded = place.replace(" ", "+")
        url = f"https://nominatim.openstreetmap.org/search?q={place_encoded}&format=json&addressdetails=0"
        r = requests.get(url, headers=headers)
        results = r.json()
        if results:
            return place, results[0]["lat"], results[0]["lon"]
        else:
            raise ValueError("Location not found.")
    else:
        raise ValueError("Location required")


def get_weather(city_country, latitude, longitude, date):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}&daily=precipitation_sum"
        f"&timezone=Europe%2FLondon&start_date={date}&end_date={date}"
    )
    response = requests.get(url)
    json_data = response.json()

    rain = json_data.get("daily", {}).get("precipitation_sum", [None])[0]

    if rain is None:
        print(f"No weather data available for {city_country} on {date}.")
    elif rain == 0.0:
        print(f"It won't rain in {city_country} on {date}.")
    else:
        print(f"It will rain in {city_country} on {date} ({rain} mm).")


def main():
    print("🌦️  Rain Forecast Program")
    print("Enter a date in YYYY-MM-DD format")
    print("Enter a location (city, country). Leave empty to quit.\n")

    weather_forecast = WeatherForecast()

    while True:
        searched_date = input("Enter date (empty for today, 'quit' to exit): ").strip()
        if searched_date.upper() == "QUIT":
            break

        if not searched_date:
            searched_date = str(datetime.date.today())
        else:
            pattern = r'^\d{4}-\d{2}-\d{2}$'
            try:
                if not re.match(pattern, searched_date):
                    raise ValueError
                datetime.datetime.strptime(searched_date, "%Y-%m-%d")
            except ValueError:
                print("Invalid date format. Using today's date instead.")
                searched_date = str(datetime.date.today())

        city_country = input("Enter city, country (or leave empty to cancel): ").strip()
        if city_country.upper() == "QUIT":
            break
        if not city_country:
            continue

        try:
            city_country, lat, lon = get_lat_long(city_country)
            weather_forecast[searched_date] = [city_country, lat, lon]
        except Exception as e:
            print(f"❌ Error: {e}")
            continue

    print("\n📅 Forecast Results:")
    for date, (city_country, lat, lon) in weather_forecast.items():
        get_weather(city_country, lat, lon, date)


if __name__ == '__main__':
    main()
