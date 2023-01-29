import io
import os
import requests
import urllib.request
from bs4 import BeautifulSoup 
import random
import string
from google.cloud import vision
from os import listdir
import stat

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
        self.avg /= (self.total - self.data[unknown])

    def add(self, input):
        if (input >= 0 and input < 6):
            self.data[input] += 1
            self.total += 1


from imageHTML import downloadImg, generateName, uploadFile

# Imports the Google Cloud client library
from google.cloud import storage

# Instantiates a storage client
storage_client = storage.Client()

#stats to be collected
adultContent = Statistic("adult")
medicalContent = Statistic("medical");
spoofedContent = Statistic("spoofed");
violentContent = Statistic("violent");
racyContent = Statistic("racy")

def cVision(safe, labels):
    #safe search check
    
    print('Safe search~\nLikelihood of image category (0-5)')

    print('adult: {}'.format(safe.adult))
    adultContent.add(safe.adult)

    print('medical: {}'.format(safe.medical))
    medicalContent.add(safe.medical)

    print('spoofed: {}'.format(safe.spoof))
    spoofedContent.add(safe.spoof)

    print('violence: {}'.format(safe.violence))
    violentContent.add(safe.violence)

    print('racy: {}'.format(safe.racy))
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

files = os.listdir(path='./resources/')
length = len(files)

# Generate name for new bucket to be made in the cloud
newBucketName = generateName(6)

# Make the bucket, will be deleted
bucket = storage_client.create_bucket(newBucketName)

# Receives a url and returns it as text
url = "https://www.google.com/search?rlz=1C1CHBF_enUS981US981&sxsrf=AJOqlzVpBO_esqGbJRtUtOQRe8MBOc0E8g:1674952087676&q=giraffe&tbm=isch&sa=X&ved=2ahUKEwjel87hwuv8AhX8SzABHZviBe0Q0pQJegQIDxAB&biw=1536&bih=714&dpr=1.25" # will be replaced with user input url
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
print(f"Bucket {newBucketName} deleted")

allStats = [adultContent,medicalContent,spoofedContent,violentContent,racyContent] 

for i in allStats:
    print("There are " + str(i.data[5]) + " images that are very likely to be " + i.cat)
    print("There are " + str(i.data[4]) + " images that are likely to be " + i.cat)
    print("There are " + str(i.data[3]) + " images that are possible to be " + i.cat)
    print("There are " + str(i.data[2]) + " images that are unlikely to be " + i.cat)
    print("There are " + str(i.data[1]) + " images that are very unlikely to be " + i.cat)
    print("There are " + str(i.data[0]) + " images that are unknown to be " + i.cat)

if (num == 0):
    print("No images found on this website.")