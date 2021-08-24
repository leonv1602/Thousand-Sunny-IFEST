from bs4 import BeautifulSoup

import requests as r

import pandas as pd

emiten_list = ["GIAA", "ANTM", "KAEF", "UNVR", "WSKT"]
for emiten in emiten_list:
    result = []
    last_page = int(BeautifulSoup(r.get(f"https://www.cnbcindonesia.com/search?query={emiten}").text).find('div', {'class': 'paging'}).find_all('a')[-2].text)
    for page in range(1,last_page+1):
        url_string = f"https://www.cnbcindonesia.com/search?query={emiten}&p={page}&kanal=&tipe=artikel&date="
        req = r.get(url_string)
        body = req.text
        soup = BeautifulSoup(body)
        result += [t['href'] for t in soup.find_all("ul")[-2].find_all('a')]
    data = []
    for url in result[len(data):]:
        req = r.get(url)
        if req.status_code == 200:
            body = req.text
            soup = BeautifulSoup(body)
            title = soup.find('h1').text
            try:
                date = soup.find('div', {'class': 'date'}).text
            except:
                date = soup.find('span', {'class': 'date'}).text
            data.append((title, date))
        else:
            data.append((None, None))
    data_dict = {'title': [], 'date': []}
    for title, date in data:
        data_dict['title'].append(title)
        data_dict['date'].append(date)
    df = pd.DataFrame(data_dict)
    df.to_csv(f'{emiten}_news_title.csv', index=False)



