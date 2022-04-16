import requests
from rich.table import Table
from rich.console import Console


class RequestManager:
    def __init__(self, TOKEN, city=None):
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
        if self.city is None:
            r = requests.get(self.BASE_URL)
        else:
            r = requests.get(self.CITY_URL)

        self.json_resp = r.json()
        return self.json_resp

    def format_data(self):
        """To do: try to find a better solution to parse json data"""
        self.current_weather_data = self.json_resp.copy()
        self.current_weather_data.pop('forecast')
        """To do: try to replace loop to a map"""
        for k,v in self.current_weather_data.items():
            if type(v) == int:
                self.current_weather_data[k] = str(v)
            else:
                continue

        self.forecast_data = {'forecast': self.json_resp['forecast']}
        """To do: try to replace loop to a map"""
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
