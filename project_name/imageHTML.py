import os
import requests
import urllib.request
from bs4 import BeautifulSoup 

# Receives a url and returns it as text
def getData(url): 
    r = requests.get(url) 
    return r.text 

# Given an image URL, downloads the image into a folder
def downloadImg(image_url, folder):
    filename = folder + "/" + image_url.split("/")[-1] 

    r = requests.get(image_url, stream = True)
    if r.ok:
        urllib.request.urlretrieve(image_url, filename)
        print("Download successful ", filename)
    else:
        print("Download failed")
    os.remove(filename)
   
htmldata = getData("https://www.geeksforgeeks.org/") 
soup = BeautifulSoup(htmldata, 'html.parser') 
for image in soup.find_all('img'):
    print(image['src'])
    downloadImg(image['src'], "images")