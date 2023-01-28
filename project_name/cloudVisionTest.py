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

# local source folder
source = './resources'

# Creates the new bucket
#bucket = storage_client.create_bucket(bucket_name)

# Instantiates a vision client
client = vision.ImageAnnotatorClient()


files = os.listdir(path='./resources/')
length = len(files)

# Generate name for new bucket to be made in the cloud
newBucketName = generateName(6)

# Make the bucket, will be deleted
bucket = storage_client.create_bucket(newBucketName)

# Receives a url and returns it as text
url = "https://geeksforgeeks.org" # will be replaced with user input url
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser') 

# For each image in html, run downloadImg
for image in soup.find_all('img'):
    image_url = image['src']
    #print(image_url)
    if(image_url != "" and image_url.find("http") != -1):
        downloadImg(image['src'], "images", newBucketName)

# List of items in cloud bucket
bucketList = bucket.list_blobs();

# Checks each image in bucket using cloud vision
for x in bucketList:
    #print('checking ' + x.name())
    content = x.download_as_bytes()
    image = vision.Image(content=content)
    labelresponse = client.label_detection(image=image)
    ssresponse = client.safe_search_detection(image=image)
    safe = ssresponse.safe_search_annotation
    labels = labelresponse.label_annotations

    # safe search check
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Safe search~\nLikelihood of image category (0-5)')

    print('adult: {}'.format(safe.adult))
    print('adult: {}'.format(likelihood_name[safe.adult]))

    print('medical: {}'.format(likelihood_name[safe.medical]))
    print('spoofed: {}'.format(likelihood_name[safe.spoof]))
    print('violence: {}'.format(likelihood_name[safe.violence]))
    print('racy: {}'.format(likelihood_name[safe.racy]))
    print('\n')

    # image labeling
    print('\nLabels~')
    for label in labels:
        print(label.description)
    print('\n')

    x.delete()


bucket = storage_client.get_bucket(newBucketName)
bucket.delete()
print(f"Bucket {newBucketName} deleted")