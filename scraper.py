from bs4 import BeautifulSoup
from selenium import webdriver
import csv
driver = webdriver.Chrome()

for num in range(388):

    driver.get(f"https://clutch.co/agencies/digital-marketing?client_type=field_pp_cs_midmarket&client_type=field_pp_cs_enterprise&page={num}")
    page = driver.page_source

    soup = BeautifulSoup(page,"lxml")

    cards = soup.find_all("div",class_="provider-info col-md-10")
    website_url = ""
    companies = []



    for card in cards:
        name = card.find("h3",class_="company_info")
        if name is not None:
            name = name.text.strip()
        location = card.find("span",class_="locality")
        if location is not None:
            location = location.text.strip()
        links = "https://clutch.co" + str(card.find("a",class_="company_title directory_profile").get("href"))
        driver2 = webdriver.Chrome()
        inside_page = driver2.get(links)
        src2 = driver2.page_source
        inside_soup = BeautifulSoup(src2,"lxml")
        website = inside_soup.find("a", {"class": "visit-website website-link__item", "title": "Visit website"})
        if website is not None:
            website = website.get("href").strip()
        
        companies.append({"Company Name":name,
                        "Website":website,
                        "Location":location})

keys = companies[0].keys()
with open("company.csv","w",newline="",encoding="UTF-8") as f:
    writer = csv.DictWriter(f,keys)
    writer.writeheader()
    writer.writerows(companies)

