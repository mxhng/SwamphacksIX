import argparse
import io
import json
import os
from textHTML import getText

# Imports the Google Cloud client library
from google.cloud import language_v1
import numpy
import six

def nlpCategorize (url):
    #Categorizes Input Text

    #Call web scraper to generate text from url
    text = getText(url)

    # Instantiates a client
    language_client = language_v1.LanguageServiceClient()

    # The text to analyze
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = language_client.classify_text(request={"document" : document})
    categories = response.categories

    result = {}

    for category in categories:
        #Turn categories into a dictionary/map of structure
        #{category.name: category.confidence}
        result[category.name] = category.confidence

    print(text)
    for category in categories:
        print("=" * 20)
        print("{:<16}: {}".format("category", category.name))
        print("{:<16}: {}".format("confidence", category.confidence))
    
    return result