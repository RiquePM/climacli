from arguments import arguments
from pathlib import Path
from clima import RequestManager, RenderWeather
from user_data import UserData


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
    if Path(UserData.path).is_file():
        args = arguments(1)
        user_data = UserData()
        if user_data.city is not None and args.city is None:
            request_manager = RequestManager(user_data.TOKEN, 
                                             city=user_data.city
                                             )
            
            sei_la(request_manager, args)
        
        elif args.city is not None:
            request_manager = RequestManager(user_data.TOKEN, 
                                             city=args.city
                                             )
            sei_la(request_manager, args)
            
        else:
            args = arguments(2)
            if args.set_city == "True":
                usr_data = UserData()
                usr_data.create_usr_file(usr_data.TOKEN, 
                                         default_city=args.city
                                         )
            
                request_manager = RequestManager(usr_data.TOKEN, 
                                                 city=usr_data.city
                                                 )
                
                sei_la(request_manager, args)

            else:
                usr_data = UserData()
                request_manager = RequestManager(usr_data.TOKEN,
                                                 city=args.city 
                                                 )
                
                sei_la(request_manager, args)
                
    else:
        args = arguments(3)
        if args.set_city == "True":
            usr_data = UserData()
            usr_data.create_usr_file(args.token, args.city)
            
            request_manager = RequestManager(usr_data.TOKEN, 
                                             city=usr_data.city
                                             )
            
            sei_la(request_manager, args)
            
        else:
            usr_data = UserData()
            usr_data.create_usr_file(args.token)
            request_manager = RequestManager(usr_data.TOKEN, 
                                             city=args.city
                                             )
            sei_la(request_manager, args)
            

if __name__ == '__main__':
    main()
