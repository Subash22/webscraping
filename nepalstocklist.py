from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq


# working with txt file to extract data
f = open('listofstocks.txt', 'w', encoding="utf-8")

# NEPSE Stocks
for sect in ['Commercial Banks', 'Finance', 'Hotels', 'Manufacturing And Processing', 'Others', 'Hydro Power', 'Tradings', 'Non Life Insurance', 'Development Banks', 'Government Bond', 'Corporate Debenture', 'Preferred Stock', 'Mutual Fund', 'Microfinance', 'Life Insurance']:
    f.write('\n' + str(sect) + ' in NEPSE\n')
    f.write('-------------------------\n')
    for page in range(1, 15):
        my_url = 'http://www.nepalstock.com/company/index/' + str(page) + '/'

        # opening the connection and grabbing the page
        uClient = uReq(my_url)
        page_html = uClient.read()
        uClient.close()

        # html parsing with BeautifulSoup
        page_soup = soup(page_html, 'html.parser')
        # grab each list
        container = page_soup.find('table', {'class': 'my-table'})
        container = container.select('tr')

        for i in range(2, 22):
            try:
                name = container[i].select_one('td:nth-child(3)').text
                symbol = container[i].select_one('td:nth-child(4)').text
                sector = container[i].select_one('td:nth-child(5)').text
                link = container[i].select_one('td:nth-child(6)').a['href']
            except:
                symbol = ''

            if sector == str(sect):
                f.write(str(symbol)+', ')

f.close()

# Commercial Banks, Finance, Hotels, Manufacturing And Processing, Others, Hydro Power, Tradings, Non Life Insurance, Development Banks, Government Bond, Corporate Debenture, Preferred Stock, Mutual Fund, Microfinance, Life Insurance
