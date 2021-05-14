from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import csv

# working with excel sheet to extract data
f = open('collegeinNepal.csv', 'a', newline='')
writer = csv.writer(f)
writer.writerow(['List of Colleges in Nepal'])
writer.writerow(['Name', 'Address', 'Phone Number', 'Email', 'Website'])

for page in range(1, 12):
    my_url = 'https://www.yellowpagesnepal.com/search?k=college&page=' + str(page)

    # opening the connection and grabbing the page
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()

    # html parsing with BeautifulSoup
    page_soup = soup(page_html, 'html.parser')
    # grab each list
    container = page_soup.findAll('li', {'class': 'list-content-section'})

    for i in container:
        link = 'https://www.yellowpagesnepal.com/' + i.find('h3').a['href']

        name = i.find('h3').text

        try:
            address = i.find('div', attrs={"class": "info-row"}).text
        except:
            address = 'Null'

        # opening the connection and grabbing the page
        uClient = uReq(link)
        page_html = uClient.read()
        uClient.close()

        # html parsing with BeautifulSoup
        page_soup = soup(page_html, 'html.parser')
        # grab each data
        container = page_soup.find('div', {'class': 'contact-content'})

        try:
            phone = container.meta['content']
        except:
            phone = 'Null'

        try:
            email = container.find("meta", itemprop="email")
            email = email['content']
        except:
            email = 'Null'

        try:
            website = container.a['href']
        except:
            website = 'Null'

        writer.writerow([name.strip(), address.strip(), phone.strip(), email.strip(), website.strip()])
        # print([name.strip(), address.strip(), phone.strip(), email.strip(), website.strip()])

f.close()
