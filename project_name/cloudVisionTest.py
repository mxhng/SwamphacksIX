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

# Collects data from images and organizes it
def cVision(safe, labels):
    #safe search check
    adultContent.add(safe.adult)
    medicalContent.add(safe.medical)
    spoofedContent.add(safe.spoof)
    violentContent.add(safe.violence)
    racyContent.add(safe.racy)

class Statistic(object):

    vLikely = 5
    likely = 4
    possible = 3
    unlikely = 2
    vUnlikely = 1
    unknown = 0

    def __init__ (self, cat):
        self.cat = cat
        self.data = [0,0,0,0,0,0]
        self.total = 0;
        self.possible = 0;

    def add(self, input):
        self.data[input] += 1
        self.total += 1


# Instantiates storage and vision clients
storage_client = storage.Client()
client = vision.ImageAnnotatorClient()

# Stats to be collected
adultContent = Statistic("adult")
medicalContent = Statistic("medical");
spoofedContent = Statistic("spoofed");
violentContent = Statistic("violent");
racyContent = Statistic("racy")
allContent = [adultContent,medicalContent,spoofedContent,violentContent,racyContent]


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
        #print(image_url)
        if(image_url != "" and image_url.find("http") != -1):
            if(image_url.split('.')[-1] != 'svg'):
                downloadImg(image['src'], "images", newBucketName, num)
                num += 1 

    # List of items in cloud bucket
    bucketList = bucket.list_blobs()

    # Checks each image in bucket using cloud vision
    for x in bucketList:
        print('checking ' + x.name)
        content = x.download_as_bytes()
        image = vision.Image(content=content)
        labelresponse = client.label_detection(image=image)
        ssresponse = client.safe_search_detection(image=image)

        checkSafe = ssresponse.safe_search_annotation
        checkLabels = labelresponse.label_annotations

        cVision(checkSafe, checkLabels)

        x.delete()


    bucket = storage_client.get_bucket(newBucketName)
    bucket.delete()



# Data output functions

# Number of images 'possibly,' 'likely,' and 'very likely' belonging to a specified sensitive category
def calcPossible():
    for i in allContent:
        i.possible = i.data[5] + i.data[4] + i.data[3]


# List numbers of 'very likely' images there are in each category
def vLikely():
    out = [adultContent.data[5],medicalContent.data[5],spoofedContent.data[5],violentContent.data[5],racyContent.data[5]]
    return out

# List numbers of 'possible' images there are in each category
def possible():
    out = [adultContent.data[3],medicalContent.data[3],spoofedContent.data[3],violentContent.data[3],racyContent.data[3]]
    return out

# List numbers of 'likely' images there are in each category
def likely():
    out = [adultContent.data[4],medicalContent.data[4],spoofedContent.data[4],violentContent.data[4],racyContent.data[4]]
    return out

# List percent (<1) of images belonging to each category per category
def percentLikely():
    calcPossible()
    return [ adultContent.possible / (adultContent.total - adultContent.data[0]),
    medicalContent.possible / (medicalContent.total - medicalContent.data[0]),
    spoofedContent.possible / (spoofedContent.total - spoofedContent.data[0]),
    violentContent.possible / (violentContent.total - violentContent.data[0]),
    racyContent.possible / (racyContent.total - racyContent.data[0])]

# Returns total amount of images processed
def total():
    return adultContent.total