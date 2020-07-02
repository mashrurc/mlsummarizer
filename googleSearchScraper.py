# BS4 Solution
import urllib
import requests
from bs4 import BeautifulSoup

# The term we want to search for
query = "Joe Joe"

# Replace all spaces of given query with '+'
query.replace(' ', '+')
URL = "https://google.com/search?q={}&".format(query)

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
headers = {"user-agent": USER_AGENT}

firstSweep = BeautifulSoup(requests.get(URL, headers=headers).content, features="html.parser")
videoTab = firstSweep.find("a", {"class": "q qs", "data-sc" : "V"})
videoLink = videoTab.get('href')

URL2 = "https://google.com{}".format(videoLink)
# print(URL2)

# Creates a GET request based on the URL, inputs the raw code for BS4 to interpret
webPage = BeautifulSoup(requests.get(URL, headers=headers).content, features="html.parser")
# print(webPage.prettify())

divTags = []
divTags = webPage.find_all("h3", {"class": "LC20lb DKV0Md"})

print(divTags)

# In order to use this, you must pay for your API key

# from serpapi import GoogleSearchResults
#
# params = {
#     "q": "Coffee",
#     "location": "Austin, Texas, United States",
#     "hl": "en",
#     "gl": "us",
#     "google_domain": "google.com",
#     "api_key": "secret_api_key"
# }
#
# client = GoogleSearchResults(params)
# results = client.get_dict()
# print(results)