import requests
from django.shortcuts import render
import datetime
from datetime import timedelta
import json
from urllib.request import urlopen


def main(request):
    if request.method == 'POST':
        city = request.POST['city']
    else:
        url = 'http://ipinfo.io/json'
        response = urlopen(url)
        data = json.load(response)
        city = data['city']

    appid = '8e498f09a55491fde5fa1d9ef9d19466'
    URL1 = 'https://api.openweathermap.org/data/2.5/weather'
    PARAMS1 = {'q': city, 'appid': appid, 'units': 'metric'}

    r = requests.get(url=URL1, params=PARAMS1).json()

    lon = r['coord']['lon']
    lat = r['coord']['lat']

    URL2 = 'https://api.openweathermap.org/data/2.5/onecall'
    PARAMS2 = {'lat': lat, 'lon': lon, 'exclude': 'current,hourly', 'appid': appid, 'units': 'metric'}

    r2 = requests.get(url=URL2, params=PARAMS2).json()

    temps = []
    descriptions = []
    icons = []
    dates = []
    next_day = datetime.date.today()

    for i in r2['daily'][1:]:
        next_day = next_day + timedelta(days=1)
        weekday = next_day.strftime('%a')
        month = next_day.strftime('%b')
        temps.append(str(i['temp']['day']) + '/' + str(i['temp']['night']))
        descriptions.append((i['weather'][0]['description']).title())
        icons.append(i['weather'][0]['icon'])
        dates.append(f'{weekday},{month} {str(next_day)[8:]}')

    another_days = zip(temps, descriptions, icons, dates)

    weather = {
        'city': city.title(),
        'temperature': r['main']['temp'],
        'description': (r['weather'][0]['description']).title(),
        'icon': r['weather'][0]['icon'],
        'another_days': another_days
    }

    context = {'weather': weather}

    return render(request, 'weather/weather.html', context)
