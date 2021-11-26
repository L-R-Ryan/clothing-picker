import random
import csv
from pyowm import OWM
import datetime
import pandas as pd

#jersey_city_id = 5099836
api_key = '<FILL THIS IN>'

owm = OWM(api_key)
mgr = owm.weather_manager()
observation = mgr.weather_at_place('Jersey City, US')
w = observation.weather

data = w.temperature('fahrenheit')
max_temp = data["temp_max"]
current_temp = data["temp"]
day = datetime.datetime.today().weekday()

if day == 6 or day == 7:
    day_type = 'weekday'
else:
    day_type = 'weekend' #using opposite meanings in here because I filter based on "not" later

if max_temp > 75:
    clothing_type = 'cold'
else:
    clothing_type = 'hot' #using opposite meanings in here because I filter on "not" later

choice = "start"

while choice == "start" or choice == "no":
    all_clothes = pd.read_csv("unused_test.csv")
    day_specific_clothes = all_clothes[all_clothes['day']!=day_type]
    temp_specific_clothes = day_specific_clothes[day_specific_clothes['weather']!=clothing_type]
    num_mean = temp_specific_clothes.num.mean()
    needs_wearing = temp_specific_clothes[temp_specific_clothes['num']<=num_mean]
    suggestion = random.choice(list(needs_wearing.item))

    index_id_all = all_clothes.index[all_clothes['item']==suggestion].tolist()[0]

    print ("Would you like to wear '%s'?" % suggestion)
    choice = input("> ")
    if choice == "no":
        print ("Would like to get rid of '%s'?" % suggestion)
        removal = input("> ")
        if removal == "yes":
            all_clothes.drop(index_id_all, axis=0, inplace=True)
            all_clothes.to_csv("unused_test.csv", index=False)
            print ("lightening your load! great job!")

if choice == "yes":
    index_loc = all_clothes.iloc[index_id_all, all_clothes.columns.get_loc('num')]
    index_loc = index_loc + 1
    all_clothes.to_csv("unused_test.csv", index=False)
    print ("You'll look great!")


print ("The temperature is currently "+str(current_temp)+" and the high will be "+str(max_temp))
