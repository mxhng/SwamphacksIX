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

def cVision(safe, labels):
    #safe search check
    adultContent.add(safe.adult)
    medicalContent.add(safe.medical)
    spoofedContent.add(safe.spoof)
    violentContent.add(safe.violence)
    racyContent.add(safe.racy)

    #image labeling
    #print('\nLabels~')
    #for label in labels:
        #print(label.description)
    #print('\n')

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
        self.avg = 0;

    def calcAverage(self):
        i = 1
        for i in range (6):
            self.avg += self.data[i] * i
        self.avg /= (self.total - self.data[0])

    def add(self, input):
        self.data[input] += 1
        self.total += 1

# Instantiates a storage client
storage_client = storage.Client()

#stats to be collected
adultContent = Statistic("adult")
medicalContent = Statistic("medical");
spoofedContent = Statistic("spoofed");
violentContent = Statistic("violent");
racyContent = Statistic("racy")
allStats = [adultContent,medicalContent,spoofedContent,violentContent,racyContent] 

# Instantiates a vision client
client = vision.ImageAnnotatorClient()

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


def vLikely():

    out = [adultContent.data[5],medicalContent.data[5],spoofedContent.data[5],violentContent.data[5],racyContent.data[5]]
    return out

def percentLikely():
    out = [ (adultContent.data[5] + adultContent.data[4] + adultContent.data[3]) / (adultContent.total - adultContent.data[0]),
    (medicalContent.data[5] + medicalContent.data[4] + medicalContent.data[3]) / (medicalContent.total - medicalContent.data[0]),
    (spoofedContent.data[5] + spoofedContent.data[4] + spoofedContent.data[3]) / (spoofedContent.total - spoofedContent.data[0]),
    (violentContent.data[5] + violentContent.data[4] + violentContent.data[3]) / (violentContent.total - violentContent.data[0]),
    (racyContent.data[5] + racyContent.data[4] + racyContent.data[3]) / (racyContent.total - racyContent.data[0])]
    return out

def total():
    return adultContent.total