from tkinter import *
import sqlite3
import requests
root=Tk()
root.resizable(0,0)


def weather_details(location):
    city_name = location
    API_key = '6b2efb27b43cb20d6c0b88c1c762b080'
    url=f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}'
    weather_response=requests.get(url)
    weather_json=weather_response.json()
    main=weather_json['main']
    humidity = main['humidity']
    weather_array= weather_json['weather']
    weather=(weather_array[0]['main'])
    temperature = main['temp']
    weather_list={'weather':weather,'humidity':humidity,'temperature':temperature}
    return weather_list



weather_label = Label(text=f"Weather: {weather_details('Kathmandu')['weather']}",anchor=W)
humidity_label = Label(text=f"Humidity: {weather_details('Kathmandu')['humidity']}",anchor=W)
temp_Label = Label(text= f"Temperature: {weather_details('Kathmandu')['temperature']}",anchor=W)


weather_label.grid(row=0,column=0,padx=2,pady=2)
humidity_label.grid(row=1,column=0,padx=2,pady=2)
temp_Label.grid(row=2,column=0,padx=2,pady=2)
root.mainloop()