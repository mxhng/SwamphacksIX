import requests
from bs4 import BeautifulSoup

def getText(url):
    #open url with GET
    resp = requests.get(url)

    #code 200 means site could be accessed
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')

        siteText = soup.get_text()
    
    return siteText
