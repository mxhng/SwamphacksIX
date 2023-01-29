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

    #sort results by confidence level (highest first)
    confidenceSortedResults = sorted(result.items(), key = lambda x:x[1], reverse = True)

    if len(result) > 3:
        confidenceSortedResultsDict = dict(confidenceSortedResults.items()[0: 3])
    else:
        confidenceSortedResultsDict = dict(confidenceSortedResults)

    for key in confidenceSortedResultsDict:
        confidenceSortedResultsDict[key] = str(round(100.0 * float(confidenceSortedResultsDict[key]), 2))
    
    return confidenceSortedResultsDict
