from bs4 import BeautifulSoup
import requests
import shutil
import pathlib

def getdata(url): 
    r = requests.get(url) 
    return r.text

fullLink = input("site: ")
comic = fullLink.replace("https://www.erofus.com", "")
site = "https://www.erofus.com"

issues = []
imgSites = []
numbers = []

soup = BeautifulSoup(getdata(fullLink), 'html.parser')
for item in soup.find_all('a'):
    if comic in item['href'] and '?' not in item['href'] and comic != item['href']:
        issues.append(item['href'])

for issue in issues:
    p = pathlib.Path('.' + comic + issue.replace(comic, ""))
    p.mkdir(parents=True, exist_ok=True)
    print("Downloading " + issue.replace("/comics/", ""))

    imgSites = []
    soup = BeautifulSoup(getdata(site + issue), 'html.parser') 
    for item in soup.find_all('a'):
        if 'pic' in item['href']:
            imgSites.append(item['href'])

    numbers = []
    for i in range(len(imgSites)):
        numbers.append(int(imgSites[i].replace("/pic/", "").replace(comic.replace("/comics", ""), "").replace(issue.replace(comic, ""), "").replace("/" + str(i + 1), "")))#int(imgSites[len(imgSites) - 1].replace("/pic/", "").replace(comic.replace("/comics", ""), "").replace(issue.replace(comic, ""), "").replace("/" + str(len(imgSites)), ""))]

    num = 0
    for number in numbers:
        num = num + 1
        pic = site + "/pic/" + str(number) + comic.replace("/comics", "") + issue.replace(comic, "") + "/" + str(num)
        soup = BeautifulSoup(getdata(pic), 'html.parser')
        for item in soup.find_all('img'):
            if 'medium' in item['src']:
                url = site + str(item['src'])
                file_name = str(num) + '.jpg'

        res = requests.get(url, stream = True)

        if res.status_code == 200:
            with open('./' + comic + "/" + issue.replace(comic, "") + "/" + file_name,'wb') as f:
                shutil.copyfileobj(res.raw, f)

print("Downloaded " + comic)
