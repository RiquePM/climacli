import requests
from rich.console import Console
from rich.table import Table
import argparse


class RequestManager:
    def __init__(self, city, TOKEN):
        """In the future these constants are going to be imported
           from another python module in order to reduce code verbosity 
        """
        self.TOKEN = TOKEN
        self.city = city
        self.FIELDS = '''only_results,temp,date,description,city,humidity,
                         forecast,date,weekday,max,min,description
                      '''

        self.BASE_URL = ''.join(f'''https://api.hgbrasil.com/weather?
                                    fields={self.FIELDS}
                                    &key={self.TOKEN}
                                 '''.split())

        self.CITY_URL = ''.join(f'''https://api.hgbrasil.com/weather?
                                    fields={self.FIELDS}
                                    &key={self.TOKEN}
                                    &city_name={self.city}
                                 '''.split())
                                 
        self.json_resp = None
        self.current_weather_data = None
        self.forecast_data = None

    def request_data(self):
        """To do: put the function inside a try-except block"""
        r = requests.get(self.CITY_URL)
        self.json_resp = r.json()
        return self.json_resp

    def format_data(self):
        """To do: """
        self.current_weather_data = self.json_resp.copy()
        self.current_weather_data.pop('forecast')
        for k,v in self.current_weather_data.items():
            if type(v) == int:
                self.current_weather_data[k] = str(v)
            else:
                continue

        self.forecast_data = {'forecast': self.json_resp['forecast']}
        for val in self.forecast_data['forecast']:
            for k, v in val.items():
                if type(v) == int:
                    val[k] = str(v)
            else:
                continue

        return self.current_weather_data, self.forecast_data

class RenderWeather:
    def __init__(self, current_weather_data, forecast_data):
        self.current_weather_data = current_weather_data
        self.forecast_data = forecast_data
        self.console = Console()

    def render_current_weather(self):
        """To do: customize the table"""
        current_weather_table = Table(
            "Temperature",
            "Date",
            "Description",
            "City",
            "Humidity",
        title=f'Current weather in {self.current_weather_data["city"]}',
        )
        current_weather_table.add_row(*self.current_weather_data.values())
        return self.console.print(current_weather_table)

    def render_forecast(self):
        """To do: customize the table"""
        forecast_table = Table(
            "Date",
            "Weekday",
            "Max",
            "Min",
            "Description",
            title=f'''{self.current_weather_data["city"]} 
                      10 day weather forecast
                   ''',
            )
        for val in self.forecast_data['forecast']:
            forecast_table.add_row(*val.values())

        return self.console.print(forecast_table)

def main():
    parser = argparse.ArgumentParser(description='''
                                                  Displays the current weather
                                                  and the next 10 day 
                                                  weather forecast for the
                                                  solicited city
                                                 '''
                                    )
    parser.add_argument('token')
    parser.add_argument('city', 
                        help="Ex: sao-paulo; brasilia")
    parser.add_argument('-f','--forecast', choices=['True', 'False'], default='False')
    args = parser.parse_args()

    request_manager = RequestManager(args.city, args.token)
    request_manager.request_data()
    request_manager.format_data()
    render_weather = RenderWeather(request_manager.current_weather_data,
                                   request_manager.forecast_data
                                  )
    render_weather.render_current_weather()
    
    if args.forecast != 'False':
        render_weather.render_forecast()
    


if __name__ == '__main__':
    main()