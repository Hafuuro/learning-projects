import requests
from bs4 import BeautifulSoup
from time import sleep
from csv import DictWriter
import os
from random import choice
from random import randint
import pandas as pd

BASE_URL = "https://speedhome.com"

rental = []
url = "/rent?pg=1"

while url:
    res = requests.get(f"{BASE_URL}{url}")
    print(f"Now scraping {BASE_URL}{url}")
    soup = BeautifulSoup(res.text, "html.parser")
    rent = soup.find_all(class_="pro-col pro-grid col-xs-12 col-sm-4")

    for home in rent:
        rental.append({
            "name":home.find(class_="pro-title").get_text(),
            "price":home.find(class_="price").get_text(),
            "features":home.find(class_="features-sub").get_text(",", strip=True).split(","),
            "facilities":[i[0] + " " + i[1] for i in list(zip(home.find(class_="facilities").get_text(",", strip=True).split(","), [i["src"][16:-4] for i in home.find(class_="facilities").find_all("img")]))],

        })
#     break
    next = soup.find(class_ = "next")
    url = next["href"] if next else None
    print("Sleeping")
    sleep(randint(10,60))

df = pd.DataFrame(rental)
df = df[["name", "price", "features", "facilities"]]
df.to_csv("data/speedhome.csv", encoding='utf-8', index=False)
