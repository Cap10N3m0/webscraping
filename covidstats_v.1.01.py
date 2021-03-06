from bs4 import BeautifulSoup
from urllib.request import urlopen
import matplotlib.pyplot as plt

page = "https://en.m.wikipedia.org/wiki/COVID-19_pandemic_by_country_and_territory"
print("\033[1m"+"\t\tCOVID-19 Pandemic Country Check"+"\033[0m")
try:
    html = urlopen(page)
except:
    print("\033[1m"+'\t\tSorry The Program Has Crashed'+"/033[0m")
    exit()
soup = BeautifulSoup(html.read(),'lxml')

flag=0
tbody = soup.select('#thetable')
tr = tbody[0].select('tr')

headers = []
cases = []
deaths = []
recv = []
for i in range(2,230):
    headers.append(tr[i].select('th')[1].a.contents[0])
    cases.append((tr[i].select('td')[0].contents[0]).strip())
    deaths.append((tr[i].select('td')[1].contents[0]).strip())
    try:
        recv.append((tr[i].select('td')[2].contents[0]).strip())
    except:
        recv.append(None)
ctry = input("Enter the country:  ")
for i in range(len(headers)):
    if headers[i] == ctry.capitalize():
        print("Number of Cases: ",cases[i])
        print("Number of Deaths: ",deaths[i])
        print("Number of Recovered Patients: ",recv[i])
        flag=1
        if(cases[i] != None and recv[i] != None and deaths[i] != None):
            plt.pie([float(cases[i].replace(',','')),float(deaths[i].replace(',','')),float(recv[i].replace(',',''))],
                    labels=["Active Cases","Deaths","Recovered"],autopct ='%1.1f%%',colors=['blue','red','green'])
            plt.show()
        
if flag==0:
    print(ctry," Not found")
