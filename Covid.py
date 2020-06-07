from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
from bs4 import BeautifulSoup
from urllib.request import urlopen
import matplotlib.pyplot as plt
import csv
import os
import datetime
from tkinter import ttk


root = Tk()
root.title("Covid Check")
root.iconbitmap('@C1.xbm')

page = "https://en.m.wikipedia.org/wiki/COVID-19_pandemic_by_country_and_territory"

#Function to check the last entry
def check():
    
    with open("Covidstats.csv",'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for line in csv_reader:
            if line[5] == str(datetime.datetime.now().date()):
                return False    
        return True

#Function to store the details
def rec(cases,deaths,recv,headers):
    
    with open("Covidstats.csv",'a') as csvfile:
        csv_writer = csv.writer(csvfile)
        for i in range(len(cases)):
            csv_writer.writerow([i+1,headers[i],cases[i],deaths[i],recv[i],datetime.datetime.now().date()])

#Function to initialize the file    
def initf(file):
    try:
        if os.stat(file).st_size > 0:
            pass
        else:
            with open(file,'w') as newfile:
                csv_writer = csv.writer(newfile)
                csv_writer.writerow(["Rank","Country","Active Cases","Deaths","Recovered Patients","Date"])

    except OSError:
        with open(file,'w') as newfile:
            csv_writer = csv.writer(newfile)
            csv_writer.writerow(["Rank","Country","Active Cases","Deaths","Recovered Patients","Date"])
            
R1 = Label(root)
Wr1 = Label(root)
Wr2 = Label(root)
Wr3 = Label(root)
Wr4 = Label(root)
Wr5 = Label(root)

Ra1 = Label(root)
Wra1 = Label(root)
Wra2 = Label(root)
Wra3 = Label(root)
Wra4 = Label(root)
Wra5 = Label(root)

#Function to compare with previous day if possible
def showd(cases,deaths,recv,rank,name):
    with open("Covidstats.csv",'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for line in csv_reader:
            k=str(line[5])
            d=str(datetime.datetime.now().date() - datetime.timedelta(days=1))
            l=str(line[1])
            if l == name and k == d:
                global R1,Wr1,Wr2,Wr3,Wr4,Wr5
                R1.forget()
                Wr1.forget()
                Wr2.forget()
                Wr3.forget()
                Wr4.forget()
                Wr5.forget()
                R1 = Label(root,text = "\nComparison with Yesterday's Statistics",fg = 'red')
                R1.configure(font = ("Helvetica", 17))
                R1.pack()
                if int(line[2])-cases<=0:
                    Wr1 = Label(root,text = "Number of new patients : "+str(cases-int(line[2])))
                    Wr1.configure(font = ("Helvetica", 17))
                    Wr1.pack()
                else:
                    Wr1 = Label(root,text = "Decrease in patients : "+str(int(line[2])-cases))
                    Wr1.configure(font = ("Helvetica", 17))
                    Wr1.pack()
                    
                Wr2 = Label(root,text = "Increase of deaths : "+str(deaths-int(line[3])))
                Wr2.configure(font = ("Helvetica", 17))
                Wr2.pack()
                Wr3 = Label(root,text = "Increase of recovered patients : "+str(recv-int(line[4])))
                Wr3.configure(font = ("Helvetica", 17))
                Wr3.pack()
                Wr4 = Label(root,text = "Current Global rank : "+str(rank))
                Wr4.configure(font = ("Helvetica", 17))
                Wr4.pack()
                Wr5 = Label(root,text = "Global rank on the previous day : "+str(line[0]))
                Wr5.configure(font = ("Helvetica", 17))
                Wr5.pack()
                
#Function to compare with previous week if possible
def showwe(cases,deaths,recv,rank,name):
    with open("Covidstats.csv",'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for line in csv_reader:
            k=str(line[5])
            d=str(datetime.datetime.now().date() - datetime.timedelta(days=7))
            l=str(line[1])
            if l == name and k == d:
                global Ra1,Wra1,Wra2,Wra3,Wra4,Wra5
                Ra1.forget()
                Wra1.forget()
                Wra2.forget()
                Wra3.forget()
                Wra4.forget()
                Wra5.forget()
                Ra1 = Label(root,text = "\nComparison with Last week's Statistics",fg = 'red')
                Ra1.configure(font = ("Helvetica", 17))
                Ra1.pack()
                if int(line[2])-cases<=0:
                    Wra1 = Label(root,text = "Number of new patients : "+str(cases-int(line[2])))
                    Wra1.configure(font = ("Helvetica", 17))
                    Wra1.pack()
                else:
                    Wra1 = Label(root,text = "Decrease in patients : "+str(int(line[2])-cases))
                    Wra1.configure(font = ("Helvetica", 17))
                    Wra1.pack()
                    
                Wra2 = Label(root,text = "Increase of deaths : "+str(deaths-int(line[3])))
                Wra2.configure(font = ("Helvetica", 17))
                Wra2.pack()
                Wra3 = Label(root,text = "Increase of recovered patients : "+str(recv-int(line[4])))
                Wra3.configure(font = ("Helvetica", 17))
                Wra3.pack()
                Wra4 = Label(root,text = "Current Global rank : "+str(rank))
                Wra4.configure(font = ("Helvetica", 17))
                Wra4.pack()
                Wra5 = Label(root,text = "Global rank on the previous week : "+str(line[0]))
                Wra5.configure(font = ("Helvetica", 17))
                Wra5.pack()


try:
    html = urlopen(page)
except:
    response = messagebox.showerror("ERROR","PROGRAM HAS FAILED")
    Label(root,text=response).pack()
    root.destroy()
    
soup = BeautifulSoup(html.read(),'lxml')

flag=0
tbody = soup.select('#thetable')
tr = tbody[0].select('tr')

headers = []
cases = []
deaths = []
recv = []

for i in range(2,229):
    headers.append(tr[i].select('th')[1].a.contents[0])
    cases.append((tr[i].select('td')[0].contents[0]).strip())
    deaths.append((tr[i].select('td')[1].contents[0]).strip())
    try:
        recv.append((tr[i].select('td')[2].contents[0]).strip())
    except:
        recv.append(None)

for i in range(len(cases)-1):
    
    cases[i] = int(cases[i].replace(',',''))
    try:
        deaths[i] = int(deaths[i].replace(',',''))
    except:
        deaths[i] = None
    try:
        recv[i] = int(recv[i].replace(',',''))
    except:
        recv[i] = None

#Creating file
initf("Covidstats.csv")

if check():
    rec(cases,deaths,recv,headers)

CL = Label(root)
DL = Label(root)
RL = Label(root)

def look(ctry):
    global CL,DL,RL
    CL.forget()
    DL.forget()
    RL.forget()
    for i in range(len(headers)):
        if headers[i] == ctry:
            CL = Label(root,text="Number of Cases: "+str(cases[i]))
            CL.configure(font = ("Helvetica", 17))
            CL.pack()

            DL = Label(root,text = "Number of Deaths: "+str(deaths[i]))
            DL.configure(font = ("Helvetica", 17))
            DL.pack()

            RL = Label(root,text="Number of Recovered Patients: "+str(recv[i]))
            RL.configure(font = ("Helvetica", 17))
            RL.pack()
            
            if(cases[i] != None and recv[i] != None and deaths[i] != None):
                showd(cases[i],deaths[i],recv[i],i+1,headers[i])
                showwe(cases[i],deaths[i],recv[i],i+1,headers[i])
                plt.pie([cases[i],deaths[i],recv[i]],
                    labels=["Active Cases","Deaths","Recovered"],autopct ='%1.1f%%',colors=['blue','red','green'])
                plt.show()

myimg = ImageTk.PhotoImage(Image.open("c3po.png"))
Label(image = myimg).pack()

TH1 = Label(root,text = "Select the Country  :")
TH1.configure(font=("Helvetica", 21))
TH1.pack()
            
ctry = StringVar()
Select = ttk.Combobox(root,textvariable = ctry,values=headers)
Select.configure(width = 40,height =2)
Select.pack()
b1 = Button(root,text="Search",command = lambda: look(Select.get()))
b1.pack()
    
root.mainloop()
