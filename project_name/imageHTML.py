import io
import os
import requests
import urllib.request
from bs4 import BeautifulSoup 
import random
import string
from google.cloud import vision

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

# Receives a url and returns it as text
def getData(url): 
    r = requests.get(url) 
    return r.text 

# Given an image URL, downloads the image into a local folder, uploads image to the cloud bucket, delete local image 
def downloadImg(image_url, folder, bucket):
    filename = folder + "/" + image_url.split("/")[-1] 

    r = requests.get(image_url, stream = True)
    if r.ok:
        urllib.request.urlretrieve(image_url, filename)
        print("Download successful ", filename)
    else:
        print("Download failed")

    #uploads to new cloud storage bucket
    uploadFile(bucket, filename, 'copy' + filename)

    os.remove(filename)