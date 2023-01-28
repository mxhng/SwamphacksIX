import io
import os
import requests
import urllib.request
from bs4 import BeautifulSoup 
import random
import string
from google.cloud import vision
from os import listdir

from imageHTML import getData, downloadImg

# Imports the Google Cloud client library
from google.cloud import storage

# Instantiates a storage client
storage_client = storage.Client()

#local source folder
source = './resources'

# Creates the new bucket
#bucket = storage_client.create_bucket(bucket_name)

# Instantiates a vision client
client = vision.ImageAnnotatorClient()


def generateName(length):
    l = string.ascii_lowercase
    resultStr = 'safescan'
    for i in range(length):
        resultStr = resultStr + random.choice(l)
    return resultStr

def uploadFile(bucket_name, source_file, new_file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(new_file_name)

    blob.upload_from_filename(source_file)
    print(f"File {source_file} uploaded to new bucket {new_file_name}.")


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
bucketList = bucket.list_blobs();

#checks each image in bucket using cloud vision
for x in bucketList:
    print('checking ' + x.name())
    content = x.download_as_bytes()
    image = vision.Image(content=content)
    labelresponse = client.label_detection(image=image)
    ssresponse = client.safe_search_detection(image=image)
    safe = ssresponse.safe_search_annotation
    labels = labelresponse.label_annotations

    #safe search check
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

    #image labeling
    print('\nLabels~')
    for label in labels:
        print(label.description)
    print('\n')

    x.delete()


bucket = storage_client.get_bucket(newBucketName)
bucket.delete()
print(f"Bucket {newBucketName} deleted")