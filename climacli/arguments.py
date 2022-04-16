import argparse


"""
To do: add optional argument to change the token
To do: change from argparse to Click_
"""
def arguments(case):
    match case:
        case 1:
            parser = argparse.ArgumentParser(description=
                                                 '''
                                                  Displays the current weather
                                                  and the next 10 day 
                                                  weather forecast for the
                                                  solicited city
                                                 '''
                                                 )
            
            parser.add_argument('--city',
                                help="Ex: sao-paulo; brasilia"
                                )

            parser.add_argument('-f','--forecast', choices=['True', 'False'], 
                                default='False'
                                )
    
            args = parser.parse_args()
            return args

        case 2:
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
            return args

        case 3:
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
            return args
