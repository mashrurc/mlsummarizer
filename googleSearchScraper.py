# BS4 Solution
import urllib
import requests
from bs4 import BeautifulSoup

# The term we want to search for
query = "Nuclear Fission"

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
webPage = BeautifulSoup(requests.get(URL2, headers=headers).content, features="html.parser")
# print(webPage.prettify())

videoTitles = []
videoLinks = []
videoList = []
videos = []

videos = webPage.find_all("div", {"class": "r"})

for video in videos:
    videoList.append([video.find("h3", {"class": "LC20lb DKV0Md"}).text, video.find("a").get("href")])
    videoTitles.append(video.find("h3", {"class": "LC20lb DKV0Md"}).text)
    videoLinks.append(video.find("a").get("href"))

print("=========== FULL VIDEO PROFILE ==================")
print("{} \n".format(videoList))
print("=========== VIDEO LINKS ==================")
print("{} \n".format(videoTitles))
print("=========== VIDEO TITLES ==================")
print("{} \n".format(videoLinks))

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