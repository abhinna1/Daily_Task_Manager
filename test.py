from tkinter import *
import sqlite3
import requests

class login_window():
    def create_userDb(self): # Create User databse to store user information
        con=sqlite3.connect('UserInfo.db')
        c=con.cursor()

        # Create table
        c.execute("""CREATE TABLE UserInfo(
        username text,
        location
        )
        """)

        con.commit()
        con.close()

    def set_userinfo(self):
        con=sqlite3.connect('UserInfo.db')
        c=con.cursor()

        # Insert user info into database
        c.execute("INSERT INTO UserInfo VALUES(:username, :location)",{
            'username':self.username_entry.get(),
            'location':self.location_entry.get()
        })
        print('added into databse')
        con.commit()
        con.close()
        root.destroy()
        self.task_win = Tk()
        task_instane.task_screen()
        self.task_win.mainloop()
    def get_userinfo(self):
        con=sqlite3.connect('UserInfo.db')
        c=con.cursor()
        c.execute("SELECT *, oid FROM UserInfo")
        record = c.fetchall()
        for userdata in record:
            print(userdata)
            return userdata

        con.commit()
        con.close()

    def delete_userinfo(self,id):
        con = sqlite3.connect('UserInfo.db')
        c = con.cursor()
        c.execute("SELECT *, oid FROM UserInfo")
        c.execute(f"DELETE FROM UserInfo WHERE oid={id}")
        con.commit()
        con.close()

    def login_window(self):
        self.login_frame = LabelFrame(text='Enter Your Details')
        self.username_lbl = Label(self.login_frame,text='Username')
        self.username_entry = Entry(self.login_frame)
        self.location_lbl = Label(self.login_frame,text='Location')
        self.location_entry = Entry(self.login_frame)
        self.login_btn = Button(text='Login',width=25,command=login_instance.set_userinfo)

        self.login_frame.grid(row=0,column=0)
        self.username_lbl.grid(row=0,column=0)
        self.username_entry.grid(row=0,column=1)
        self.location_lbl.grid(row=1,column=0)
        self.location_entry.grid(row=1,column=1)
        self.login_btn.grid(row=2,column=0,columnspan=2)

class task_window():
    def get_weather(self):
        userdata=login_instance.get_userinfo()
        location=userdata[1]
        weather_key = '6b2efb27b43cb20d6c0b88c1c762b080'
        url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_key}'
        weather_response = requests.get(url)
        weather_json = weather_response.json()
        main = weather_json['main']
        humidity = main['humidity']
        weather_array = weather_json['weather']
        weather = (weather_array[0]['main'])
        temperature_kelvin = main['temp']
        temperature_celcius = (temperature_kelvin - 273.15)//1
        weather_info = {'weather': weather, 'humidity': humidity, 'temperature': temperature_celcius}
        return weather_info

    def weather_window(self):
        user_info = login_instance.get_userinfo()
        weather_dict = (task_window()).get_weather()
        self.weather_frame = LabelFrame(text=f'Current Weather in {user_info[1]}', font=('Areal',12))
        self.weather_label = Label(self.weather_frame, text=f"Weather: {weather_dict['weather']}", font=('Areal',11))
        self.temperature_label = Label(self.weather_frame, text=f"Temperature: {weather_dict['temperature']}", font=('Areal',11))
        self.humidity_label = Label(self.weather_frame, text=f"Humidity: {weather_dict['humidity']}", font=('Areal',11))
        print(weather_dict['weather'])

        self.weather_frame.grid(row=0,column=0)
        self.weather_label.grid(row=0,column=0)
        self.temperature_label.grid(row=1, column=0)
        self.humidity_label.grid(row=2, column=0)

    def task_window(self):
        self.taskInput_frame = LabelFrame(text='Enter your task')
        self.taskInput_lbl = Label(self.taskInput_frame,text= 'Task')
        self.task_entry = Entry(self.taskInput_frame,width=20)
        self.task_btn= Button(self.taskInput_frame,text='Add Task')

        self.taskInput_lbl.grid( row=0, column=0)
        self.task_entry.grid(row=0, column=1)
        self.task_btn.grid(row=0, column=2)
        self.taskInput_frame.grid(row=0,column=1,padx=20,pady=0)

    def task_screen(self):
        task_instane.weather_window()
        task_instane.task_window()



#class instances
login_instance=login_window()
task_instane=task_window()

# list indexings
user_info=login_instance.get_userinfo()

root=Tk()
root.title('Task Manager')
root.resizable(0, 0)

print(login_instance.get_userinfo())
# login_instance.delete_userinfo(1)
if user_info==None:
    login_instance.login_window()
else:
    task_instane.task_screen()
# print(task_instane.get_weather())
root.mainloop()