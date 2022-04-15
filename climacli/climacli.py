import requests
from rich.table import Table
from rich.console import Console
import argparse
from pathlib import Path
import usr_config_file_tst

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

def sei_la(request_manager, args):
    request_manager.request_data()
    request_manager.format_data()
    render_weather = RenderWeather(request_manager.current_weather_data,
                                   request_manager.forecast_data
                                   )
    render_weather.render_current_weather()

    if args.forecast == 'True':
        render_weather.render_forecast()


def main():
    if Path('usr_confg_file_tst.json').is_file():
        user_conf = usr_config_file_tst.read_usr_file()
        if user_conf["default_city"] is not None:
            parser = argparse.ArgumentParser(description='''
                                                  Displays the current weather
                                                  and the next 10 day 
                                                  weather forecast for the
                                                  solicited city
                                                 '''
                                                 )

            parser.add_argument('-f','--forecast', choices=['True', 'False'], 
                                default='False'
                                )
    
            args = parser.parse_args()

            request_manager = RequestManager(user_conf["TOKEN"], 
                                             city=user_conf["default_city"]
                                             )
            
            sei_la(request_manager, args)
            
        else:
            parser = argparse.ArgumentParser(description='''
                                                  Displays the current weather
                                                  and the next 10 day 
                                                  weather forecast for the
                                                  solicited city
                                                 '''
                                                 )
    
            parser.add_argument('city',
                                help="Ex: sao-paulo; brasilia"
                                )
    
            parser.add_argument('--set_city', choices=['True', 'False'], 
                                default='False', 
                                help="Store the current city as default"
                                )
    
            parser.add_argument('-f','--forecast', choices=['True', 'False'], 
                                default='False'
                                )
    
            args = parser.parse_args()
            
            if args.set_city == "True":
                user_conf = usr_config_file_tst.read_usr_file()
                usr_config_file_tst.create_usr_file(user_conf["TOKEN"], 
                                                    default_city=args.city
                                                    )
            
                request_manager = RequestManager(user_conf["TOKEN"], 
                                                 city=user_conf["default_city"]
                                                 )
                
                sei_la(request_manager, args)

            else:
                request_manager = RequestManager(user_conf["TOKEN"],
                                                 city=args.city 
                                                 )
                
                sei_la(request_manager, args)
                
    else:
        parser = argparse.ArgumentParser(description='''
                                                  Displays the current weather
                                                  and the next 10 day 
                                                  weather forecast for the
                                                  solicited city
                                                 '''
                                                 )
    
        parser.add_argument('token')
        parser.add_argument('city',
                            help="Ex: sao-paulo; brasilia"
                            )
    
        parser.add_argument('--set_city', choices=['True', 'False'], 
                            default='False', 
                            help="Store the current city as default"
                            )
    
        parser.add_argument('-f','--forecast', choices=['True', 'False'], 
                            default='False'
                            )
    
        args = parser.parse_args()
    
        if args.set_city == "True":
            usr_config_file_tst.create_usr_file(args.token, 
                                                default_city=args.city
                                                )
            
            user_conf = usr_config_file_tst.read_usr_file()
            request_manager = RequestManager(user_conf["TOKEN"], 
                                             city=user_conf["default_city"]
                                             )
            
            sei_la(request_manager, args)
            
        else:
            usr_config_file_tst.create_usr_file(args.token)
            user_conf = usr_config_file_tst.read_usr_file()
            request_manager = RequestManager(user_conf["TOKEN"], 
                                             city=args.city
                                             )
            
            sei_la(request_manager, args)
            

if __name__ == '__main__':
    main()