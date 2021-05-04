from tkinter import *
import sqlite3
import requests
root=Tk()
bg_color='PeachPuff2'
root.config(bg=bg_color)
root.resizable(0,0)
root.title('Daily Routine')

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
    temperature_kelvin = main['temp']
    temperature_celcius = temperature_kelvin - 273.15
    weather_list={'weather':weather,'humidity':humidity,'temperature':temperature_celcius}
    return weather_list

def login():
    login_frame=LabelFrame(text='Enter User Details',bg=bg_color)
    login_frame.grid(row=0,column=0)

    username_lbl=Label(login_frame,text = 'Enter Name',font=('Helvetica',10),bg=bg_color,anchor=W)
    username_lbl.grid(row=0,column=0)
    location_lbl=Label(login_frame,text = 'Enter Location',font=('Helvetica',10),bg=bg_color,anchor=W)
    location_lbl.grid(row=1,column=0,padx=4,pady=4)

    location_entry=Entry(login_frame,width=30)
    username_entry=Entry(login_frame,width=30)
    username_entry.grid(row=0,column=1,padx=4,pady=4,columnspan=3)
    location_entry.grid(row=1,column=1,padx=4,pady=4,columnspan=3)

    press_button=Button(text='Login',width=20,bg='PeachPuff3', command=new_window)
    press_button.grid(row=2,column=0,columnspan=2)
def new_window():
    global root
    root.destroy()
    info_win=Tk()
    weather_label(info_win)
    info_win.mainloop()
def weather_label(surface):
    outer_label=LabelFrame(surface,text="Current Weather",font=('Helvetica',8),bg='PeachPuff2',fg='Black')
    weather_label = Label(outer_label,text=f"Weather: {weather_details('Kathmandu')['weather']}",font=('Helvetica',12),anchor=W,bg=bg_color)
    humidity_label = Label(outer_label,text=f"Humidity: {weather_details('Kathmandu')['humidity']}",font=('Helvetica',12),anchor=W,bg=bg_color)
    temp_Label = Label(outer_label,text= f"Temperature: {weather_details('Kathmandu')['temperature']}°C",font=('Helvetica',12),anchor=W,bg=bg_color)

    outer_label.grid(row=0,column=0)
    weather_label.grid(row=1,column=0,padx=2,pady=2)
    temp_Label.grid(row=2,column=0,padx=2,pady=2)
    humidity_label.grid(row=3,column=0,padx=2,pady=2)



if __name__=='__main__':
    login()
root.mainloop()