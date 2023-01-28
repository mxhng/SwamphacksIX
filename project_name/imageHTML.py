import requests

html = (requests.get(url = 'https://www.tutorialrepublic.com/codelab.php?topic=faq&file=javascript-get-current-url').text) 
print(html.rfind("img"))

def Occurances(str, word):
    count = 0
    while(str.rfind(word) != -1):
        count = count + 1
        str = str[str.rfind(word)]


    return count	

# Driver code
print(html)
print(Occurances(html, "img"))
