import io
import os
from google.cloud import vision
from os import listdir

# Imports the Google Cloud client library
from google.cloud import storage

# Instantiates a storage client
#storage_client = storage.Client()

#local source folder
source = './resources'

# The name for the new bucket
#bucket_name = "mmhbucket"
#main_bucket = storage_client.bucket(bucket_name)

# Creates the new bucket
#bucket = storage_client.create_bucket(bucket_name)

# Instantiates a client
client = vision.ImageAnnotatorClient()

files = os.listdir(path='./resources/')
length = len(files)

#add images to cloud (doesnt work yet)
#for i in files:
    #upload_blob('./resources/'+i, main_bucket, './resources/'+i)


#looks at all images in folder 'resources'
for i in files:
    with io.open('./resources/'+i, 'rb') as image_file:

        content = image_file.read()
        image = vision.Image(content=content)
        labelresponse = client.label_detection(image=image)
        ssresponse = client.safe_search_detection(image=image)
        safe = ssresponse.safe_search_annotation
        labels = labelresponse.label_annotations

        #data output starts
        print('Data for ' + i + ':')

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