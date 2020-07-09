#from PyDictionary import PyDictionary
import wikipedia
import keywordGen

keywords = ["Nuclear Fusion", "Hitachi", "nuclear reactors", "Uranium fuel", "climate change"]
info = []
for w in keywords:
    info.append(wikipedia.summary(w, sentences=3))


print("============================WIKI SUMMARY===================================")
print(info)
print("===========================================================================")

#pip install wikipedia

# dictionary=PyDictionary()

# print(dictionary.meaning("fission"))