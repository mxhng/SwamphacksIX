import io
import os
import requests
import urllib.request
from bs4 import BeautifulSoup 
import random
import string

from google.cloud import vision
from google.cloud import storage


# Generate unique bucket ID to make a new bucket
# Done every time a new URL is submitted, bucket deleted later
def generateName(length):
    l = string.ascii_lowercase
    resultStr = 'safescan'
    for i in range(length):
        resultStr = resultStr + random.choice(l)
    return resultStr


# Given unique bucket ID, upload local file into the bucket
def uploadFile(bucket_name, source_file, new_file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(new_file_name)

    blob.upload_from_filename(source_file)
    print(f"File {source_file} uploaded to new bucket {new_file_name}.")

# Given an image URL, downloads the image into a local folder, uploads image to the cloud bucket, delete local image 
def downloadImg(image_url, folder, bucket, num):
    filename = folder + "/" + str(num) + '.jpg'

    r = requests.get(image_url, stream = True)
    if r.ok:
        urllib.request.urlretrieve(image_url, filename)
        print("Download successful ", filename)
    else:
        print("Download failed")

    #uploads to new cloud storage bucket
    uploadFile(bucket, filename, 'copy' + filename)

    os.remove(filename)