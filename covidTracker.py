# import requests
# import json

# r = requests.get(
#     'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode=488001&date=31-05-2021')

# package_json = r.json()

# # print("------------------------------------------------------------------------------------------------------------------")

# # print(package_json)

# # print("------------------------------------------------------------------------------------------------------------------")

# for x in package_json["sessions"]:
#     if(x["min_age_limit"] == 18):
#         print("Vaccine Slot Available")
#         print(f'Slots Available:{x["available_capacity_dose1"]}+')
#         break

# # package_str = json.dumps(package_json["sessions"], indent=2)

# # print(package_str)

# import time
# from datetime import datetime,timedelta

# dayDates = []
# today = datetime.today().date()
# print("----------------------------------------------------------------")
# dayDates.append(today.strftime("%d%m%Y"))
# dates = []
# for i in range(0, 7):
#     day = today + timedelta(days=i)
#     x = str(day)
#     x = x.split("-")
#     x.reverse()
#     dates.append("-".join(x))

# import winsound
# winsound.PlaySound("noti.wav", winsound.SND_FILENAME)

from os import SEEK_CUR
from tkinter import *
from bs4 import BeautifulSoup
from functools import partial
import requests
import json
from selenium import webdriver
import time
from datetime import datetime, timedelta
import winsound

root = Tk()

root.geometry("800x800")

# DATE GENERATOR:--------------------------------------------------------------------------------------------------------------------------------------
dayDates = []
today = datetime.today().date()
dayDates.append(today.strftime("%d%m%Y"))
dates = []
for i in range(0, 7):
    day = today + timedelta(days=i)
    x = str(day)
    x = x.split("-")
    x.reverse()
    dates.append("-".join(x))


# ----------------------Option Menu Of Vaccine Finder-------------------------
optionsDose = StringVar(root)
doseOptions = ["dose1", "dose2"]
optionsDose.set(doseOptions[0])
dropDose = OptionMenu(root, optionsDose, *doseOptions)

optionsAge = StringVar(root)
ageOptions = ["18+", "45+"]
optionsAge.set(ageOptions[0])
dropAge = OptionMenu(root, optionsAge, *ageOptions)

optionDate = StringVar(root)
dayOptions = dates
optionDate.set(dayOptions[0])
dropDate = OptionMenu(root, optionDate, *dayOptions)

# ----------------------------------------------------------------------------

# ---------------------------------------Covid Data Of Countries----------------------------------------------------------------------


covidData = requests.get('https://www.worldometers.info/coronavirus/').text
soup = BeautifulSoup(covidData, 'lxml')
figures = soup.find_all('div', class_='maincounter-number')


canvas = Canvas(root, width=150, height=150)
canvas.pack()
img = PhotoImage(file="fin.png")
canvas.create_image(20, 20, anchor=NW, image=img)

e = Entry(root, width=60, fg="black", bg="cyan", borderwidth=3)
e.pack()


def getCountryData():
    country = e.get()
    url = f'https://www.worldometers.info/coronavirus/country/{country}/'
    htmlText = requests.get(url).text
    soup = BeautifulSoup(htmlText, 'lxml')
    figures = soup.find_all('div', class_='maincounter-number')

    label1.config(text=country.capitalize())
    label2.config(text=f'Total Cases: {figures[0].span.text}')
    label3.config(text=f'Total Deaths: {figures[1].span.text}')
    label4.config(text=f'Total Recovered: {figures[2].span.text}')

# --------------------------------------------------------------------------------------------------------------------------------------


pin = Entry(root, width=30, fg="black", bg="white", borderwidth=3)

vcA = Label(root, text=f"",
            fg="#00b300", font=("Arial", 16))


def RUN():
    pincode = pin.get()
    date = optionDate.get()
    age = optionsAge.get()
    age = age[0:len(age)-1]
    dose = optionsDose.get()
    r = requests.get(
        f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={pincode}&date={date}')
    package_json = r.json()
    for x in package_json["sessions"]:
        if(x["min_age_limit"] == int(age) and x[f'available_capacity_{dose}'] > 0):
            print("Slots are now available, Go Book FAST!!!")
            return True

    return False


def CHECK():
    while(RUN() != True):
        time.sleep(5)
        pass
    winsound.PlaySound("noti.wav", winsound.SND_FILENAME)


check = Button(root, text="Notify Me When Available!", command=CHECK)


def findvac():
    available = False
    totalSlots = 0
    pincode = pin.get()
    age = optionsAge.get()
    age = age[0:len(age)-1]
    dose = optionsDose.get()
    date = optionDate.get()
    r = requests.get(
        f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={pincode}&date={date}')
    package_json = r.json()
    for x in package_json["sessions"]:
        if(x["min_age_limit"] == int(age) and x[f'available_capacity_{dose}'] > 0):
            totalSlots = totalSlots + x[f"available_capacity_{dose}"]
            available = True
    # check.pack()
    if(available):
        check.pack_forget()
        vcA.config(
            text=f'Vaccine Slots Available: {totalSlots} \n \n GO BOOK ON "cowin.gov.in"!!', fg="#00b300")
        vcA.pack()
        return

    vcA.config(text="Slots Not Available", fg="#ff0000")
    vcA.pack()
    check.pack()


def vaccineFinder():
    label5 = Label(root, text="Enter Pin Code:").pack()
    pin.pack()
    dropDose.pack()
    dropAge.pack()
    dropDate.pack()
    myButton3 = Button(root, text="Check Availability",
                       command=partial(findvac)).pack()


myButton1 = Button(root, text="Get Country Data",
                   command=partial(getCountryData)).pack()


label1 = Label(root, text="WorlWide", font=('Arial', 25))
label1.pack()
label2 = Label(root, text=f'Total Cases: {figures[0].span.text}', font=(
    'Arial', 16), fg="#8000ff")
label2.pack()
label3 = Label(root, text=f'Total Deaths: {figures[1].span.text}', font=(
    'Arial', 16), fg="#ff0000")
label3.pack()
label4 = Label(root, text=f'Total Recovered: {figures[2].span.text}', font=(
    'Arial', 16), fg="#00b300")
label4.pack()

myButton2 = Button(root, text="Vaccine availability",
                   command=vaccineFinder).pack()

root.mainloop()
