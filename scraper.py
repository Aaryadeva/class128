from http.server import executable
import time
import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import requests

#bs4 is used to scrap the web page as HTML it is the python module which
#is famously used for parsing of text as HTML and then performing action
#specific function and finding specific HTML tags with a particular class
#id and listing out all the <li> tags from the <ul> tags

#selenium is used in testing the functionality of website and aslo used
#used to interact with page such as clicking the button

START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"
#provide the path to chromedriver to browser
browser = webdriver.Chrome(executable_path=r"C:\Users\rajee\Desktop\game\web scraper\chromedriver.exe")
#guiding the browser to start with the URL
browser.get(START_URL)
#providing sleep time for the system so that the page is loaded completely
time.sleep(10)
planet_data = []
new_planet_data = []
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date"]


def scrape():
#create empty list so that all the data will be saved as needed to create csv file
    
#before we need to find all li tags in ul tags 
#and we need to extract the li tags using bs4
    for i in range(0, 198):
        soup = BeautifulSoup(browser.page_source, "html.parser")
    #earlier the chrome window we opened with selenium and named it as browser
    #now we are creating a bs4 object as soup in which we are passing the
    #browser page source and asking bs4 to use html parser to read
    #page as HTML

    #finding all ul tags with class name exoplanet
        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
#enumerate is a function that returns the index along with the element
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            hyperlink_li_tag=li_tags[0]
            temp_list.append('https://exoplanets.nasa.gov'+hyperlink_li_tag.find_all('a',href=True)[0]['href'])
            planet_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        print(f'{i}page done 1')

def scrap_more_data(hyperlink):
    try:
        page=requests.get(hyperlink)
        soup = BeautifulSoup(browser.page_source, "html.parser")
    #earlier the chrome window we opened with selenium and named it as browser
    #now we are creating a bs4 object as soup in which we are passing the
    #browser page source and asking bs4 to use html parser to read
    #page as HTML

    #finding all tr tags with class name exoplanet
        for tr_tag in soup.find_all("tr", attrs={"class", "fact_row"}):
            td_tags = tr_tag.find_all("td")
            temp_list = []
#enumerate is a function that returns the index along with the element
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div",attrs={"class", "fact_row"})[0].contents[0])
                except:
                    temp_list.append("")
            new_planet_data.append(temp_list)
    except:
        time.sleep(1)
        scrap_more_data(hyperlink)

scrape()

for index,data in enumerate(planet_data):
    scrap_more_data(data[5])
    print(f'{index+1}page done 2')

final_planet_data=[]

for index,data in enumerate(planet_data):
    new_planet_data_element=new_planet_data[index]
    new_planet_data_element=[elem.replace('\n','')for elem in new_planet_data_element]
    final_planet_data.append(data+new_planet_data_element)

with open("scrapper_2.csv", "w") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(final_planet_data)
