import requests
from bs4 import BeautifulSoup
import pandas as pd

###############################################################################
#define functions to scrape various sites
###############################################################################
#nfl.com
def dl_nfl_mock(url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)
    picknum = soup.findAll('p', class_='rank')
    players = soup.findAll('span', class_='team-name')
    teams = soup.findAll('div', class_='pr-header')
    
    #parse downloaded data
    pick = list()
    team = list()
    plyr = list()
    pos = list()
    new = list()
    
    for element in picknum:
        pick.append(element.text)
        
    for element in teams:
        new = element.a.get('href')
        team.append(new[(new.find('=')+1):])
        
    for element in players:
        plyr.append(element.text[:element.text.find(' -')])
        pos.append(element.text[element.text.find(' - ')+3:])
    
    author = url[url.find('article')+8:url.find('2020')-1]
    df = pd.DataFrame(data = {'pick': pick, 'team': team, 'plyr': plyr, 'pos': pos, 'author': author, 'site': 'nfl.com'})
    return df 
    
#walter football
def dl_wf(url):
    #download data from urls
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)
    
    team = list()
    plyr = list()
    pos = list()
    newline=''
    init = soup.findAll('li')
    for each in init:
        if each.findAll('b')!=[]:
            newline = each.find('b').text
            team.append(newline.split(':')[0].lstrip())
            plyr.append(newline[newline.find(': ') + 1 : newline.find(',')].lstrip())
            pos.append(newline.split(',')[1].lstrip())

    author = 'walter-football'
    df = pd.DataFrame(data = {'TEAM': team, 'PLYR': plyr, 'POS': pos, 'AUTHOR': author, 'SITE': 'walterfootball.com'})
    return df
        
def dl_cbs(url):
    #download data from urls
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)
    
    #parse downloaded data
    pick = list()
    team = list()
    plyr = list()
    pos = list()
    author = list()

    tbls = soup.findAll('div', class_='scrollable-table')
    for tbl in tbls:
        body = tbl.find('tbody').findAll('tr')
        for each in body:
            if each.find('td', class_='cell-light-text cell-rank') != None:
                pick.append(each.findAll('td')[0].text.strip())
                team.append(each.findAll('td')[2].a['href'].split('/')[5])
                plyr.append(each.findAll('td')[3].a.text.strip())
                pos.append(each.findAll('td')[4].text.strip())
                
    a = soup.findAll('a', class_='author-name')
    for each in a:
        for i in range(1,33):
            author.append(each.span.text)
        
    df = pd.DataFrame(data = {'pick': pick, 'team': team, 'plyr': plyr, 'pos': pos, 'author': author, 'site': 'cbs.com'})
    return df

#sb nation
def dl_sbnation(url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)
    h3 = soup.findAll('h3')
    pick = list()
    plyr = list()
    team = list()
    pos = list()
    
    for each in h3:
        if each.a != None:
            pick.append(each.text.split('.')[0])
            team.append(each.text.split('. ')[1].split(':')[0])
            plyr.append(each.text.split(': ')[1].split(',')[0])
            pos.append(each.text.split(', ')[1])
    df = pd.DataFrame(data = {'PICK': pick, 'TEAM': team, 'PLYR': plyr, 'POS': pos, 'AUTHOR': 'dan kadar', 'SITE': 'sbnation'})
    return df
    
#pro football focus
def dl_pff(url, author):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data) 
    h3 = soup.findAll('h3')[:-1]
    pick = list()
    team = list()
    pos = list()
    plyr = list()
        
    for each in h3:
        pick.append(each.text.split('.')[0])
        team.append(each.a.text)
        if each.text.find("— ") == -1:
            pos.append(each.text.split(", ")[1].split(" ")[0].strip())
            plyr.append(each.text.split(",")[1].strip()[each.text.split(",")[1].strip().find(" "):].strip())
        else:
            pos.append(each.text[each.text.find("— ")+2:each.text.find(" ", each.text.find("— ")+3)].strip())
            plyr.append(each.text.split("— ")[1].split(",")[0][each.text.split("— ")[1].split(",")[0].find(" "):].strip())
    df = pd.DataFrame(data = {'pick': pick, 'team': team, 'plyr': plyr, 'pos': pos, 'author': author, 'site': 'PFF'})
    return df

#pro football focus analytics - same host site, slightly different fomatting
def dl_pff_analytics(url, author):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data) 
    h3 = soup.findAll('h3')[:-1]
    pick = list()
    team = list()
    pos = list()
    plyr = list()
    pos_list = list(['QB', 'WR', 'RB', 'TE', 'OT', 'OG', 'C', 'S', 'Edge', 'CB', 'Playmaker', 'LB'])
        
    for each in h3:
        pick.append(each.text.split('.')[0])
        team.append(each.a.text)
        for p in pos_list:
            if each.text.split("– ")[1].find(' ' + p + ' ') > 0:
                pos.append(p)
                pos_split = ' ' + p + ' '
                break
        plyr.append(each.text.split("– ")[1].split(pos_split)[0].strip())
    
    df = pd.DataFrame(data = {'pick': pick, 'team': team, 'plyr': plyr, 'pos': pos, 'author': author, 'site': 'PFF'})
    return df            

#consensus mocks
def dl_consensus(url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data) 
    pick_cont = soup.findAll('div', class_='pick-number-container')
    plyr_cont = soup.findAll('div', class_='player-name')
    team_cont = soup.findAll('div', class_='pick-container')
    pos_cont = soup.findAll('div', class_='player-details')
    pick = list()
    team = list()
    pos = list()
    plyr = list()

    for (pk, pl, tm, ps) in zip(pick_cont, plyr_cont, team_cont, pos_cont):
        pick.append(pk.text)
        plyr.append(pl.text)
        team.append(tm.a['href'].split('/')[2].replace('-',' '))
        pos.append(ps.text.split(' | ')[0].strip())

    df = pd.DataFrame(data = {'pick': pick, 'team': team, 'plyr': plyr, 'pos': pos, 'author': 'consensus', 'site': 'nflmockdraftdatabase'})
    return df

#espn.com - behind an insider paywall, may need to update the cookies section
def dl_espn(url, login, pw):
    #login
    payload = {'loginValue': login, 'password': pw}
    post_headers = {'authority': 'registerdisney.go.com',
                'method': 'POST',
                'path': '/jgc/v6/client/ESPN-ONESITE.WEB-PROD/guest/login?langPref=en-US',
                'scheme': 'https',
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'authorization': 'APIKEY PefPqXqJo7bGQimAPv2vHstJsVi1KwS0K7yQf7m7X5Y8BoFPAlRpVSKLhrS+rkOlBZEOlvjG5vtmmvCah2PnOYVFOFHl',
                'cache-control': 'no-cache',
                'content-length': '48',
                'content-type': 'application/json',
                'conversation-id': '0b079a27-2c83-47bb-a8b3-05c01aa70550',
                'correlation-id': '47ed9ec6-4f78-4f6f-9842-1177c0bf36fc',
                'device-id': '6c2a7740-28d0-4bf4-873d-ec2846b26c5f',
                'expires': '-1',
                'oneid-reporting': 'eyJzb3VyY2UiOiJlc3BuIiwiY29udGV4dCI6ImRpcmVjdCJ9',
                'origin': 'https://cdn.registerdisney.go.com',
                'pragma': 'no-cache',
                'referer': 'https://cdn.registerdisney.go.com/v2/ESPN-ONESITE.WEB-PROD/en-US?include=config,l10n,js,html&scheme=https&postMessageOrigin=https%3A%2F%2Fwww.espn.com%2F&cookieDomain=www.espn.com&config=PROD&logLevel=INFO&topHost=www.espn.com&ageBand=ADULT&countryCode=US&cssOverride=https%3A%2F%2Fsecure.espncdn.com%2Fcombiner%2Fc%3Fcss%3Ddisneyid%2Fcore.css&responderPage=https%3A%2F%2Fwww.espn.com%2Flogin%2Fresponder%2Findex.html&buildId=170ea811a3e',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'}
    


    get_headers = {'authority': 'www.espn.com',
                    'method': 'GET',
                    'path': '/nfl/draft2020/insider/story/_/id/28970129/2020-nfl-mock-draft-todd-mcshay-post-free-agency-prediction-rounds-1-2',
                    'scheme': 'https',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9',
                    'cache-control': 'max-age=0',
                    'cookie': 's_ecid=MCMID%7C83185920763478590083385347019384122920; UNID=07db7a6a-8c53-4a02-9480-5aab87c854cd; UNID=07db7a6a-8c53-4a02-9480-5aab87c854cd; ESPN-ONESITE.WEB-PROD-ac=XUS; s_fid=7079DA68FF9D24C0-07F8245DCDC3BB60; AMCV_25823F955A99D5040A495C1D%40AdobeOrg=-330454231%7CMCIDTS%7C18333%7CMCMID%7C83486905455843711433338919496742173615%7CMCAAMLH-1584492691%7C7%7CMCAAMB-1584492691%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1583895091s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.1.2; s_vi=[CS]v1|2F341B090515B05C-40000841E0C0883B[CE]; country=us; AMCVS_EE0201AC512D2BE80A490D4C%40AdobeOrg=1; s_cc=true; s_c6=1584883794381-Repeat; edition-view=espn-en-us; edition=espn-en-us; region=unknown; _dcf=1; cookieMonster=1; connectionspeed=full; tveAuth=; _cb_ls=1; _cb=BBMf5rBvwGGZQ6KaN; _v__chartbeat3=DYbOmfx2YcEBq1h-s; _nr=0; trc_cookie_storage=taboola%2520global%253Auser-id%3D792e71f7-3045-44d5-bc32-3b6778c93c8d-tuct556f45b; _omnicwtest=works; tveMVPDAuth=; device_33c7ac1f=6c2a7740-28d0-4bf4-873d-ec2846b26c5f; DE2="dXNhO29oO2NvbHVtYnVzO2NhYmxlOzU7NDs0OzUzNTszOS45OTstODMuMDQ7ODQwOzM2OzEzNzs2O3VzOw=="; DS="cnIuY29tOzczNzQwMTtjaGFydGVyIGNvbW11bmljYXRpb25zOw=="; userZip=43212; AMCV_EE0201AC512D2BE80A490D4C%40AdobeOrg=-330454231%7CMCIDTS%7C18360%7CMCMID%7C83185920763478590083385347019384122920%7CMCAAMLH-1586919168%7C7%7CMCAAMB-1586919168%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1586321568s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.1.2; s_c24_s=Less%20than%201%20day; _cb_svref=null; s_omni_lid=%5B%5BB%5D%5D; espn_s2=AEAzGHUGEhAPWC9Wla3vx8qU26nJObxeoXt0x7YFWBFmHKrESbUkP1hjNxdMrzXI1Mt2n56Xp6fo0Q25OuPorMAHXF7UHhxCefQctNCZXhuobcCjxUQPfIAb%2FIH5iQVZ8RZv4o9kSMBnwIrRGvckPcvbQR1XX%2F%2Bm%2F%2BwDfQKRtDm3MEQT6Ts5Wp9VJn%2FfNux6YKTOpaniqpyKfC2ytPG77tgjkeAUfiQA%2B9OroQqE939EXyVQbjg4EHNdZzhDZu%2BKSjI54OsxNgQRyUZUdrqW27B1; ESPN-ONESITE.WEB-PROD.api=WIDXvO5w4tcRMjM3htwVUN1KCwu96W1NIHiAhOxI0JGfHWtds/aKktpNVwXme6UxUpnb3hUNzAEe/9HUHG+/xeXUBWvA; ESPN-ONESITE.WEB-PROD.ts=2020-04-08T04:11:53.798Z; ESPN-ONESITE.WEB-PROD.token=5=eyJhY2Nlc3NfdG9rZW4iOiJkOWMxNWM5MWY1MWU0ZmJlYTEyMDMzMjlhOTY5MTk4NyIsInJlZnJlc2hfdG9rZW4iOiI4MzBjNDQzZDJiYjU0ZTkwODgyY2Y3MTNjMGIxYWMyNyIsInN3aWQiOiJ7OEMwMTU4NkEtRjQ2Qy00NjIzLThCREEtNThBMkExQUU3OUUzfSIsInR0bCI6ODY0MDAsInJlZnJlc2hfdHRsIjoxNTU1MjAwMCwiaGlnaF90cnVzdF9leHBpcmVzX2luIjoxNzk5LCJpbml0aWFsX2dyYW50X2luX2NoYWluX3RpbWUiOjE1ODYzMTczMTI2MjUsInNzbyI6bnVsbCwiYXV0aGVudGljYXRvciI6ImRpc25leWlkIiwibG9naW5WYWx1ZSI6bnVsbCwiY2xpY2tiYWNrVHlwZSI6bnVsbCwic2Vzc2lvblRyYW5zZmVyS2V5IjoidU9tTWxXYm9XTWRwSUtKU3E3Rk10czhPdmtBS1VIRUpiVW12TEs2aEdBOWwzaU9QMmx2VzFpZjlFOHcwbFlETzlqME05bG9wUmVXOVl6VU1uZ3pvbTROUWwxZE0vU09WVC8wREtkM053eFBOT3Z2dm1Wdz0iLCJjcmVhdGVkIjoiMjAyMC0wNC0wOFQwMzo0MTo1My43OTVaIiwibGFzdENoZWNrZWQiOiIyMDIwLTA0LTA4VDAzOjQxOjUzLjc5NVoiLCJleHBpcmVzIjoiMjAyMC0wNC0wOVQwMzo0MTo1My43OTVaIiwicmVmcmVzaF9leHBpcmVzIjoiMjAyMC0xMC0wNVQwMzo0MTo1My43OTVaIiwiYmx1ZV9jb29raWUiOm51bGx9|eyJraWQiOiJ3UnlKZXlYTi9iODdwamFySDVOaldCcEpzV1dJZXREZlZMeVZyNDRJRXlrPSIsImFsZyI6IlJTMjU2In0.eyJpc3MiOiJodHRwczovL2F1dGhvcml6YXRpb24uZ28uY29tIiwic3ViIjoiezhDMDE1ODZBLUY0NkMtNDYyMy04QkRBLTU4QTJBMUFFNzlFM30iLCJhdWQiOlsidXJuOmJhbXRlY2g6c2VydmljZTphY2NvdW50IiwiRVNQTi1PTkVTSVRFLldFQi1QUk9EIl0sImV4cCI6MTU4NjQwMzcxMiwiaWF0IjoxNTg2MzE3MzEyLCJqdGkiOiJSTXhVMWFWTlVBZFAyM3hBX2xfNDFRIiwibmJmIjoxNTg2MzE3MjUyLCJhX3R5cCI6Ik9ORUlEX1NFQ1VSRSIsImFfY2F0IjoiR1VFU1QiLCJhdHIiOiJkaXNuZXlpZCIsImNfdGlkIjoiMTMyNCJ9.bDoyXSJdGNmQOIarOseo1B547bLyFZrCyjLCYx3Y0QspiHGiQnaBZnn_HDM50HNWpv3mewexjTdRQqEII4PcGeRAU3UlRmEgg-182WOuy7Kd6mjbcz7RR67U2GHqMW4b6La_HSLkGhRFEEKXaWHE1BFPaKMIb4Hu5l6ukbB1v3IsWS96DdB4RKnljrsgdJ49Gj2meq31_fHYIITkaRhI_Fo1ZNGBbl04UXICjkAnya2UhH0FYFcRcp9iP7zc2edZTFQf21PkgR21dDnzh3rALo9arRBXE_mJDCNJWJGbtottiUsfoNZYSf8KOJRP0eEXvKse5_YWdeTAmQA5N5Vypg; ESPN-ONESITE.WEB-PROD.idn=00bd2ac9c5; SWID_NT=0; SWID={8C01586A-F46C-4623-8BDA-58A2A1AE79E3}; espnAuth={"swid":"{8C01586A-F46C-4623-8BDA-58A2A1AE79E3}"}; dtcAuth=ESPN_PLUS; s_sq=%5B%5BB%5D%5D; s_gpv_pn=espn%3Anfl%3Adraft2020%3Ainsider%3Astory; block.check=true%7Cfalse; s_c24=1586318229334; _chartbeat2=.1583260285384.1586318229528.1000000000000001.CPpCbUBYS9l7DjiMVQCXUr_xCuQv1l.30',
                    'if-none-match': 'W/"0f656f2a3f60387da9ad40dd98ea4f30e73d60b2"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'}

    with requests.Session() as s:
        post = s.post('https://www.espn.com/login', data = payload, headers = post_headers)
        url_dl = 'https://www.espn.com/nfl/draft2020/insider/story/_/id/28970129/2020-nfl-mock-draft-todd-mcshay-post-free-agency-prediction-rounds-1-2'
        r = requests.get(url_dl, headers = get_headers)        
        data = r.text
        soup = BeautifulSoup(data)        
        
    h2 = soup.findAll('h2')
    b = soup.findAll('b')
    p = soup.findAll('p')
    
    pick = list()
    plyr = list()
    team = list()
    pos = list()
    
    for each in h2:
        if each.a != None:
            if len(each.text.split('.')[0].strip().split(' ')) < 6:
                pick.append(each.text.split('.')[0].strip())
                team.append(each.a.text)

    for each in p:
        if (each.text.find(',') >= 0) & (each.text.find('\n') < 0) & (each.a != None) & ((each.b != None) | (each.strong != None)):
            if each.a['href'].find('/player/') > 0:
                #plyr.append(each.text.split(',')[0].strip())
                plyr.append(each.a.text)
                #pos.append(each.text.split(',')[1].strip())
                pos.append(each.text.split(',')[1].strip())
    
    df = pd.DataFrame(data = {'PICK': pick, 'PLYR': plyr, 'TEAM': team, 'POS': pos, 'AUTHOR': 'todd mcshay', 'SITE': 'ESPN'})
    return df
    