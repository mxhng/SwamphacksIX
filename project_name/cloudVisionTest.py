import io
import os
import requests
import urllib.request
from bs4 import BeautifulSoup 
import random
import string
from google.cloud import vision
from os import listdir

from imageHTML import getData, downloadImg, generateName, uploadFile

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

#local source folder
source = './resources'

# Creates the new bucket
#bucket = storage_client.create_bucket(bucket_name)

# Instantiates a vision client
client = vision.ImageAnnotatorClient()

files = os.listdir(path='./resources/')
length = len(files)

#generate name for new bucket to be made in the cloud
newBucketName = generateName(6)

#make the bucket, will be deleted
bucket = storage_client.create_bucket(newBucketName)

#get html data
htmldata = getData("https://en.wikipedia.org/wiki/Red-eared_slider") #will be replaced with user input url
soup = BeautifulSoup(htmldata, 'html.parser') 

#for each image in html, run downloadImg
for image in soup.find_all('img'):
    #print(image['src'])
    downloadImg(image['src'], "images", newBucketName)

#list of items in cloud bucket
bucketList = bucket.list_blobs()

#amount of images files uploaded to cloud bucket
totalImgs = len(bucketList)

#checks each image in bucket using cloud vision
for x in bucketList:
    print('checking ' + x.name())
    content = x.download_as_bytes()
    image = vision.Image(content=content)
    labelresponse = client.label_detection(image=image)
    ssresponse = client.safe_search_detection(image=image)
    checkSafe = ssresponse.safe_search_annotation
    checkLabels = labelresponse.label_annotations

    vision(checkSafe)

    x.delete()


bucket = storage_client.get_bucket(newBucketName)
bucket.delete()
print(f"Bucket {newBucketName} deleted")

if (totalImgs == 0):
    print("No images found on this website.")