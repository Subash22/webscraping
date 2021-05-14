from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from openpyxl import Workbook

# Variables
lifeInsurance = ['ALICL', 'GLICL', 'LICN', 'NLICL', 'NLIC', 'PLIC', 'RLI', 'SLICL']
nonlifeinsurance = ['AIL', 'EIC', 'GIC', 'HGI', 'IGI', 'LGIL', 'NIL', 'NICL', 'NLG', 'PRIN', 'PIC', 'PICL', 'RBCL', 'SIC', 'SGI', 'SICL', 'SIL', 'UIC']
commercialBanks = ['ADBL', 'BOKL', 'CCBL', 'CZBIL', 'CBL', 'EBL', 'GBIME', 'HBL', 'JBNL', 'KBL', 'LBL', 'MBL', 'MEGA', 'NABIL', 'NBB', 'NBL', 'NCCB', 'NIB', 'SBI', 'NICA', 'NMB', 'PRVU', 'PCBL', 'SANIMA', 'SBL', 'SCB', 'SRBL']
developmentBanks = ['BHBL', 'CORBL', 'DBBL', 'EDBL', 'GBBL', 'GRDBL', 'HAMRO', 'JBBL', 'KEBL', 'KSBBL', 'KADBL', 'KNBL', 'KRBL', 'LBBL', 'MLBL', 'MDB', 'MNBBL', 'NABBC', 'NCDB', 'NIDC', 'ODBL', 'PURBL', 'SHBL', 'SBBLJ', 'SAPDBL', 'SADBL', 'SHINE', 'SINDU', 'TMDBL']
hyderPower = ['AKJCL', 'API', 'AKPL', 'AHPC', 'BARUN', 'BPCL', 'CHL', 'CHCL', 'DHPL', 'GHL', 'HDHPC', 'HURJA', 'HPPL', 'JOSHI', 'KPCL', 'KKHC', 'LEC', 'MHNL', 'NHPC', 'NHDL', 'NGPL', 'PMHPL', 'PPCL', 'RADHI', 'RRHP', 'RHPL', 'RHPC', 'SHPC', 'SJCL', 'SSHL', 'SPDL', 'UNHPL', 'UMHL', 'UPCL', 'UPPER']
finance = ['BFC', 'CMB', 'CFCL', 'CEFL', 'CFL', 'GFCL', 'GMFIL', 'GUFL', 'HATH', 'HFL', 'ICFC', 'JFL', 'JEFL', 'LFC', 'MFIL', 'MPFL', 'NFS', 'NSM', 'PFL', 'PROFL', 'RLFL', 'SFC', 'SFCL', 'SIFC', 'SFFIL', 'SYFL', 'UFL']
microFinance = ['ACLBSL', 'AKBSL', 'AMFI', 'ALBSL', 'CBBL', 'CLBSL', 'DDBL', 'FMDBL', 'FOWAD', 'GMFBS', 'GGBSL', 'GILB', 'GBLBS', 'GLBSL', 'ILBS', 'JSLBB', 'KMCDB', 'LLBS', 'MSMBS', 'MSLB', 'MERO', 'MMFDB', 'MLBBL', 'NADEP', 'NBBL', 'NMFBS', 'NAGRO', 'NSEWA', 'NLBBL', 'NICLBSL', 'NUBL', 'NMBMF', 'NLBSL', 'RMDC', 'RSDC', 'SABSL', 'SDLBSL', 'SMATA', 'SLBSL', 'SKBBL', 'SNLB', 'SPARS', 'SMFDB', 'SMB', 'SLBS', 'SWBBL', 'SMFBS', 'SDESI', 'SLBBL', 'USLB', 'VLBS', 'WOMI']
manufacturingAndProcessing = ['AVU', 'BSL', 'BNL', 'BNT', 'BSM', 'FHL', 'GRU', 'HBT', 'HDL', 'JSM', 'NBBU', 'NKU', 'NLO', 'NVG', 'RJM', 'SHIVM', 'SBPP', 'SRS', 'UNL']
hotels = ['OHL', 'SHL', 'TRH', 'YHL']
tradings = ['BBC', 'NTL', 'NWC', 'STC']
others = ['CIT', 'HIDCL', 'NTC', 'NFD', 'NRIC', 'NRN']

sectors = [lifeInsurance, nonlifeinsurance, commercialBanks, developmentBanks, hyderPower, finance, microFinance, manufacturingAndProcessing, hotels, tradings, others]

book = Workbook()

for sector in range(11):
    if sector == 0:
        sname = 'Life Insurance'
    elif sector == 1:
        sname = 'Non-life Insurance'
    elif sector == 2:
        sname = 'Commercial Banks'
    elif sector == 3:
        sname = 'Development Banks'
    elif sector == 4:
        sname = 'Hydro Power'
    elif sector == 5:
        sname = 'Finance'
    elif sector == 6:
        sname = 'Micro-Finance'
    elif sector == 7:
        sname = 'Manufacturing and Processing'
    elif sector == 8:
        sname = 'Hotels'
    elif sector == 9:
        sname = 'Tradings'
    else:
        sname = 'Others'

    # working with excel sheet
    book.create_sheet(sname)
    sheet = book.get_sheet_by_name(sname)
    # sheet.autoFitColumn(3)
    try:
        book.remove_sheet(book.get_sheet_by_name("Sheet"))
        print(sname)
    except:
        print(sname)
    sheet.append(['Name', 'Symbol', 'EPS', 'P/E Ratio', '1 Year Yield', 'Market Capitalization', 'Bonus Share', 'Cash Dividend'])

    # NEPSE Stocks
    for symbl in sectors[sector]:
        my_url = 'https://merolagani.com/CompanyDetail.aspx?symbol=' + str(symbl)

        # opening the connection and grabbing the page
        uClient = uReq(my_url)
        page_html = uClient.read()
        uClient.close()

        # html parsing with BeautifulSoup
        page_soup = soup(page_html, 'html.parser')
        # grab each list
        container = page_soup.find('table', {'id': 'accordion'})
        symbol = str(symbl)

        try:
            name = page_soup.select_one('#ctl00_ContentPlaceHolder1_CompanyDetail1_companyName').text
        except:
            name = ''
        try:
            eps = container.select_one('tbody:nth-child(10) > tr > td').text.replace('\r', '').replace('\n', '').replace(' ', '')
        except:
            eps = ''
        try:
            pe = container.select_one('tbody:nth-child(11) > tr > td').text
        except:
            pe = ''
        try:
            yy = container.select_one('tbody:nth-child(9) > tr > td').text
        except:
            yy = ''
        try:
            mc = container.select_one('tbody:nth-child(18) > tr > td').text
        except:
            mc = ''
        try:
            cd = container.select_one('tbody:nth-child(14) > tr > td').text.replace('\r', '').replace('\n', '').replace(' ', '')
        except:
            cd = ''
        try:
            bs = container.select_one('tbody:nth-child(15) > tr > td').text.replace('\r', '').replace('\n','').replace(' ', '')
        except:
            bs = ''

        rows = [name.strip(), symbol.strip(), eps.strip(), pe.strip(), yy.strip(), mc.strip(), bs.strip(), cd.strip()]
        print(rows)
        sheet.append(rows)

    book.save("FundamentalAnalysis\\fundamentalAnalysis.xlsx")
