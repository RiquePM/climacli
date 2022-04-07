import requests
from rich.console import Console
from rich.table import Table
import argparse


def request_data(URL):
    r = requests.get(URL)
    return r.json()

def format_data(json_resp):
    current_weather_data = json_resp.copy()
    current_weather_data.pop('forecast')
    for k,v in current_weather_data.items():
        if type(v) == int:
            current_weather_data[k] = str(v)
        else:
            continue

    forecast_data = {'forecast': json_resp['forecast']}
    for val in forecast_data['forecast']:
        for k, v in val.items():
            if type(v) == int:
                val[k] = str(v)
        else:
            continue

    return current_weather_data, forecast_data

def render_current_weather(json_resp):
    console = Console()
    current_weather_data = format_data(json_resp)[0]
    current_weather_table = Table(
        "Temperature",
        "Date",
        "Description",
        "City",
        "Humidity",
    title=f'Current weather in {current_weather_data["city"]}',
    )
    current_weather_table.add_row(*current_weather_data.values())
    return console.print(current_weather_table)

def render_forecast(json_resp):
    console = Console()
    current_weather, forecast_data = format_data(json_resp)
    forecast_table = Table(
        "Date",
        "Weekday",
        "Max",
        "Min",
        "Description",
        title=f'{current_weather["city"]} 10 day weather forecast',
        )
    for val in forecast_data['forecast']:
        forecast_table.add_row(*val.values())
    
    return console.print(forecast_table)

def main(city, display_forecast):
    TOKEN = 'user token here'
    CITY = f'{city}'
    FIELDS = '''only_results,temp,date,description,city,humidity,forecast,date,
            weekday,max,min,description'''
    URL1 = f'''https://api.hgbrasil.com/weather?fields={FIELDS}
               &key={TOKEN}&city_name={CITY}
            '''
    URL2 = f'https://api.hgbrasil.com/weather?fields={FIELDS}&key={TOKEN}'

    json_resp = request_data(URL2)
    render_current_weather(json_resp)
    if display_forecast:
        render_forecast(json_resp)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
                                                  Displays the current weather
                                                  and the next 10 day 
                                                  weather forecast for the
                                                  solicited city
                                                 '''
                                    )
    parser.add_argument('city')
    parser.add_argument('--forecast')
    args = parser.parse_args()
    
    main(args.city, args.forecast)