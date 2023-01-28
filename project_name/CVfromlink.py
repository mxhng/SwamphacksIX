import io
import os
import random
import string

from google.cloud import vision
from os import listdir

# Imports the Google Cloud client library
from google.cloud import storage

# Instantiates a storage client
storage_client = storage.Client()

#test
import urllib.request
from PIL import Image
  
urllib.request.urlretrieve(
  'https://media.geeksforgeeks.org/wp-content/uploads/20210318103632/gfg-300x300.png',
   "gfg.png")
  
#img = Image.open("gfg.png")
#img.tobytes("xbm", "rgb")

#local source folder
source = 'https://img.youtube.com/vi/FsbYh47q55o/maxresdefault.jpg'
def uploadFile(bucket_name, source_file, new_file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(new_file_name)

    blob.upload_from_filename(source_file)
    print(f"File {source_file} uploaded to new bucket {new_file_name}.")

uploadFile('mmhbucket', 'gfg.png', '1')


# Creates the new bucket
#bucket = storage_client.create_bucket(bucket_name)

# Instantiates a vision client
client = vision.ImageAnnotatorClient()

content = img
image = vision.Image(content=content)
labelresponse = client.label_detection(image=image)
ssresponse = client.safe_search_detection(image=image)
safe = ssresponse.safe_search_annotation
labels = labelresponse.label_annotations

#data output starts
#print('Data for ' + x.name + ':')

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

