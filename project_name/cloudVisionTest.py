import io
import os
import requests
import urllib.request
from bs4 import BeautifulSoup 
import random
import string
from google.cloud import vision
from os import listdir

from imageHTML import downloadImg, generateName, uploadFile

# Imports the Google Cloud client library
from google.cloud import storage

# Instantiates a storage client
storage_client = storage.Client()

#stats to be collected
adultContent = Stat(adult)
medicalContent = Stat(medical);
spoofedContent = Stat(spoofed);
violentContent = Stat(violent);
racyContent = Stat(racy)

def vision(safe, labels):
    #safe search check
    
    print('Safe search~\nLikelihood of image category (0-5)')

    print('adult: {}'.format(safe.adult))
    adultContent.add(safe.adult)

    print('medical: {}'.format(safe.medical))
    medicalContent.add(safe.medical)

    print('spoofed: {}'.format(safe.spoof))
    spoofedContent.add(safe.spoof)

    print('adult: {}'.format(safe.violence))
    violentContent.add(safe.violence)

    print('adult: {}'.format(likelihood_name[safe.racy]))
    racyContent.add(safe.racy)


    print('\n')

    #image labeling
    print('\nLabels~')
    for label in labels:
        print(label.description)
    print('\n')

# local source folder
source = './resources'

# Creates the new bucket
#bucket = storage_client.create_bucket(bucket_name)

# Instantiates a vision client
client = vision.ImageAnnotatorClient()

<<<<<<< Updated upstream
files = os.listdir(path='./resources/')
length = len(files)
=======
def main(url):
    # Generate name for new bucket to be made in the cloud
    newBucketName = generateName(6)

    # Make the bucket, will be deleted
    bucket = storage_client.create_bucket(newBucketName)

    # Receives a url and returns it as text
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    num = 0
    for image in soup.find_all('img'):
        image_url = image['src']
        print(image_url)
        if(image_url != "" and image_url.find("http") != -1):
            downloadImg(image['src'], "images", newBucketName, num)
            num += 1 

    # List of items in cloud bucket
    bucketList = bucket.list_blobs()
>>>>>>> Stashed changes

# Generate name for new bucket to be made in the cloud
newBucketName = generateName(6)

# Make the bucket, will be deleted
bucket = storage_client.create_bucket(newBucketName)

# Receives a url and returns it as text
url = "https://www.airbnb.co.uk/s/Bratislava--Slovakia/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&place_id=ChIJl2HKCjaJbEcRaEOI_YKbH2M&query=Bratislava%2C%20Slovakia&checkin=2020-11-01&checkout=2020-11-22&source=search_blocks_selector_p1_flow&search_type=search_query" # will be replaced with user input url
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

# For each image in html, run downloadImg
num = 0
for image in soup.find_all('img'):
    image_url = image['src']
    print(image_url)
    if(image_url != "" and image_url.find("http") != -1):
        downloadImg(image['src'], "images", newBucketName, num)
        num += 1 

# List of items in cloud bucket
bucketList = bucket.list_blobs()

#amount of images files uploaded to cloud bucket
totalImgs = len(bucketList)

# Checks each image in bucket using cloud vision
for x in bucketList:
    print('checking ' + x.name())
    content = x.download_as_bytes()
    image = vision.Image(content=content)
    labelresponse = client.label_detection(image=image)
    ssresponse = client.safe_search_detection(image=image)

<<<<<<< Updated upstream
    checkSafe = ssresponse.safe_search_annotation
    checkLabels = labelresponse.label_annotations

    vision(checkSafe)
=======
def vLikely():
    out = [adultContent.data[5],medicalContent.data[5],spoofedContent.data[5],violentContent.data[5],racyContent.data[5]]
    return out

def percentLikely():
    out = [0,0,0,0,0]
    x = 0
    for i in allStats:
        out[x] = ( x.data[5] + x.data[4] + x.data[3] ) / x.total
    return out

>>>>>>> Stashed changes

    x.delete()


bucket = storage_client.get_bucket(newBucketName)
bucket.delete()
print(f"Bucket {newBucketName} deleted")

if (totalImgs == 0):
    print("No images found on this website.")