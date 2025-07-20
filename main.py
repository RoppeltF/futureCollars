import datetime
import geocoder
import requests
import re

def get_lat_long(place):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'X-Custom-Header': 'Hello World',
        'Accept-Language': 'en-US,en;q=0.9'
    }

    if place:

#         GEOCODER DOESN'T WORK SEEMS TO NEED AN API, AND  I'M NOT ADDING MY CC TO GOOGLE
#         g = geocoder.google(place)
#         print(g)
#         return g.latlng
#       As ALTERNATIVE I'M using the bellow code USL used -- https://gridreferencefinder.com found  the niminatim... to get lat long info.


        place = place.replace(" ","+")

        url = f"https://nominatim.openstreetmap.org/search?q={place}&format=json&addressdetails=0"
        r = requests.get(url,headers=headers)
        results = r.json()

        return place,results[0]["lat"],results[0]["lon"]
    else:
        g = geocoder.ip('me')


        url = f"https://nominatim.openstreetmap.org/reverse?lat={g.latlng[0]}&lon={g.latlng[1]}&format=jsonv2"
        r = requests.get(url,headers=headers)
        results = r.json()
        city = results["address"]["city"]

        return city,g.latlng[0],g.latlng[1]

def get_weather(api_data):

    city_country,latitude,longitude,searched_date = api_data.split(',')
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=precipitation_sum&timezone=Europe%2FLondon&start_date={searched_date}&end_date={searched_date}"
    rsession = requests.Session()
    response = rsession.get(url)
    json = response.json()

    if json['daily']['precipitation_sum'][0] == 0.0:
        print( f"it won't rain in {city_country} at {searched_date} ")
    elif json['daily']['precipitation_sum'][0] > 0.0:
        print( f"it will rain in {city_country} at {searched_date} ")
    else:
        print(f"Weather not available for: {city_country}")


def main():
    print("Please enter date in YYYY-MM-DD format meaning - Year 4 digits, Month 2 digits, Day 2 digits")
    print("Please enter place to check the Weather as city, country - Ex. London")
    print("Type QUIT to stop adding places to check the Weather at date info or city info")
    api_data = []

    while True:

        print("\n")
        searched_date = input("Please enter date (empty for today's date - quit to exit) : ")

        if searched_date.upper() == "QUIT":
            break

        if searched_date:
            pattern = r'^\d{4}-\d{2}-\d{2}$'
            date_format = "%Y-%m-%d"
            if re.match(pattern, searched_date):
                try:
                    datetime.datetime.strptime(searched_date, date_format)
                except ValueError:
                    print("Invalid date, using today as date instead")
                    searched_date = datetime.date.today()
            else:
                print("Invalid date, using today as date instead")
                searched_date = datetime.date.today()
        if not searched_date:
            searched_date = datetime.date.today()

        print("\n")
        city_country = input("Please enter City and Country to check weather (empty local weather - quit to exit): ")
        if city_country.upper() == "QUIT":
            break


        city_country,latitude,longitude = get_lat_long(city_country)
        api_data.append(f"{city_country},{latitude},{longitude},{searched_date}")
        print(api_data)


    print("\nCollected Data:")
    for data in api_data:
        get_weather(data)


if __name__ == '__main__':
    main()