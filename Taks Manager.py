from tkinter import *
import sqlite3
import requests

class manager:
    def create_database(self): #Run function to create database file
        self.connection = sqlite3.connect('UserBase.db')
        self.c = self.connection.cursor()
        self.c.execute("""CREATE TABLE userDetails(
        username text,
        address text
        )""")
        self.connection.commit()
        self.connection.close()

    def clear_database(self):
        self.connection4 = sqlite3.connect('UserBase.db')
        self.cursor4 = self.connection4.cursor()
        self.cursor4.execute("SELECT *, oid FROM userDetails")
        data = self.cursor4.fetchall()
        self.delete_query= """DELETE FROM userDetails where oid=1"""
        self.cursor4.execute(self.delete_query)
        for info in data:
            print(info)
        self.connection4.commit()
        self.cursor4.close()

    #Login Window
    def login(self):
        def set_info():  # stores user information in the database
            edit_connection = sqlite3.connect('UserBase.db')
            cursor2 = edit_connection.cursor()
            cursor2.execute("INSERT INTO userDetails VALUES(:username, :location)",
                                 {
                                     'username': self.username_entry.get(),
                                     'location': self.location_entry.get()
                                 })
            edit_connection.commit()
            edit_connection.close()

        # Window Design
        self.info1_lbl = LabelFrame(text='Enter your information')
        self.username_lbl = Label(self.info1_lbl,text = 'Username')
        self.location_lbl = Label(self.info1_lbl,text = 'Location')
        self.username_lbl.grid(row=0, column=0,padx=4,pady=2)
        self.location_lbl.grid(row=1, column=0,padx=4,pady=2)

        self.username_entry = Entry(self.info1_lbl)
        self.location_entry = Entry(self.info1_lbl)
        self.username_entry.grid(row=0,column=1,padx=4,pady=2)
        self.location_entry.grid(row=1,column=1,padx=4,pady=2)
        self.info1_lbl.grid(row=0,column=0,padx=4,pady=2)

        self.login_btn = Button(text='Log In',width=20,command=set_info)
        self.login_btn.grid(row=2, column=0, columnspan=2)



    def get_weather(self,location): #takes weather details from API
        self.location = location
        self.weather_key = '6b2efb27b43cb20d6c0b88c1c762b080'
        url = f'https://api.openweathermap.org/data/2.5/weather?q={self.location}&appid={self.weather_key}'
        weather_response = requests.get(url)
        weather_json = weather_response.json()
        main = weather_json['main']
        self.humidity = main['humidity']
        weather_array = weather_json['weather']
        self.weather = (weather_array[0]['main'])
        temperature_kelvin = main['temp']
        self.temperature_celcius = temperature_kelvin - 273.15
        self.weather_info = {'weather': self.weather, 'humidity': self.humidity, 'temperature': self.temperature_celcius}
        return self.weather_info

    def weather_window(self):
        self.weather_frame=LabelFrame(text='Current Weather')
        self.weather_dict=(manager()).get_weather('Kathmandu')
        self.weather_lbl=Label(self.weather_frame,text=f"Weather: {self.weather_dict['weather']}")
        self.temp_lbl=Label(self.weather_frame,text=f"Temperature:{self.weather_dict['temperature']}",anchor=W)
        self.humid_lbl= Label(self.weather_frame,text= f"Humidity: {self.weather_dict['humidity']}",anchor=W)

        self.weather_frame.grid(row=0, column=0)
        self.weather_lbl.grid(row=0,column=0)
        self.temp_lbl.grid(row=2, column=0)
        self.humid_lbl.grid(row=1,column=0)

        self.clear_btn = Button(text='Clear', command=(instance.clear_database))

        self.clear_btn.grid(row=10, column=0)

    def get_details(self):
        self.connection3 = sqlite3.connect('UserBase.db')
        self.cursor3 = self.connection3.cursor()
        self.cursor3.execute("SELECT *, oid FROM userDetails")
        data = self.cursor3.fetchall()
        for info in data:
            return info

    def create_task_db(self):
        connect = sqlite3.connect('TaskBase.db')
        cursor = connect.cursor()
        cursor.execute("""CREATE TABLE taskList(
        tasks text
        )""")
        connect.commit()
        cursor.close()

    def set_task(self):
        connect = sqlite3.connect('TaskBase.db')
        cursor =connect.cursor()

        cursor.execute("INSERT INTO taskList VALUES(:task)",{
            'task':self.task_entry.get()
        })

        connect.commit()
        connect.close()

    def task_menu(self):
        # connect task database
        connect = sqlite3.connect('TaskBase.db')
        cursor = connect.cursor()

        self.taskEntry_frame = LabelFrame(text='Add Tasks')
        self.task_entry = Entry(self.taskEntry_frame)
        self.Enter_task_lbl = Label(self.taskEntry_frame,text='Enter Task')
        self.add_taks_btn = Button(self.taskEntry_frame,text='Add Task',command=instance.set_task)

        self.Enter_task_lbl.grid(row=0,column=0,padx=3,pady=3)
        self.task_entry.grid(row=0,column=1,padx=3,pady=3)
        self.taskEntry_frame.grid(row=0,column=1,padx=10,pady=5)
        self.add_taks_btn.grid(row=0,column=2,padx=10,pady=3)

        self.task_frame = LabelFrame(text='Tasks')

        cursor.execute("SELECT *, oid FROM taskList")
        record=cursor.fetchall()
        print(record)
        for item in record:
            for taskrow in range(0, len(record)):
                self.task_lbl = Label(self.task_frame, text=item, width=30)
                self.task_lbl.grid(row=taskrow, column=0, columnspan=3)

        connect.commit()
        connect.close()

root=Tk()
root.title('Task Manager')
instance=manager()

# if len(instance.get_details())==0:
instance.weather_window()
instance.task_menu()
instance.get_details()
# else:
#     instance.login()
root.mainloop()