from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import csv

# working with excel sheet to extract data
f = open('developmentbanksinnepal.csv', 'w', newline='')
writer = csv.writer(f)
writer.writerow(['List of Commercial Banks in Nepal'])
writer.writerow(['Name', 'Address', 'Phone Number', 'Email', 'Other Branches'])

for page in range(1, 12):
    my_url = 'https://nepalyellowpages.net/search/results/' + str(page) + '?search=bank&location=all&category=all'

    # opening the connection and grabbing the page
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()

    # html parsing with BeautifulSoup
    page_soup = soup(page_html, 'html.parser')
    # grab each list
    container = page_soup.findAll('div', {'class': 'item-container'})

    for i in container:
        link = i.find('h4').a['href']

        name = i.find('h4').text
        tag = i.find('span', {'class': 'item-category'}).text

        if tag == '#BANKS (DEVELOPMENT)':

            # opening the connection and grabbing the page
            uClient = uReq(link)
            page_html = uClient.read()
            uClient.close()

            # html parsing with BeautifulSoup
            page_soup = soup(page_html, 'html.parser')
            # grab each data
            container = page_soup.select_one('body > section > div > div:nth-child(3) > div.col-md-9.col-sm-8.col-xs-12 > div')

            mainbranch = container.find('div', {'class': 'col-md-8'})
            subbranches = container.find('div', {'class': 'col-md-12'})

            try:
                address = mainbranch.select_one('li').text.strip()
                address = address.split('\n')
                address = address[1].strip()
            except:
                address = 'Null'

            try:
                phone = mainbranch.select_one('li:nth-child(2)').text.strip()
                phone = phone.split('\n')
                phone = phone[1].strip()
            except:
                phone = 'Null'

            try:
                email = mainbranch.select_one('li:nth-child(3)').text.strip()
                email = email.split('\n')
                email = email[1].strip()
            except:
                email = 'Null'

            # grab each list
            branches = subbranches.findAll('div', {'class': 'branch'})
            branchDetails = []

            for count in range(len(branches)):

                bname = branches[count].find('h4').find('strong').text.strip()
                bdetails = branches[count].find('ul').text.strip()
                bdetails = bdetails.replace('\t', '')
                bdetails = bdetails.replace('\n\n', '\t')
                bdetails = bdetails.replace('\n', '')
                bdetails = bdetails.replace('\t', '\n')
                bdetails = bdetails.replace(':', ': ')
                bdetails = bdetails.replace('  ', ' ')

                branchDetails.append(bname + '\n\n' + bdetails)

            branchDetails.insert(0, name)
            branchDetails.insert(1, address)
            branchDetails.insert(2, phone)
            branchDetails.insert(3, email)

            # [branchDetails[count] for count in range(len(branches))]
            writer.writerow(branchDetails)
            # print([name.strip(), address.strip(), phone.strip(), website.strip()])

f.close()
