# =========================IMPORTS=========================#

# import word frequency and keyword extraction libraries
from wordfreq import zipf_frequency, word_frequency
from gensim.summarization import keywords

# Sample Text
text = "Nuclear power is a clean and efficient way of boiling water to make steam, which turns turbines to produce " \
       "electricity. Nuclear power plants use low-enriched uranium fuel to produce electricity through a process " \
       "called fission the splitting of uranium atoms in a nuclear reactor. Uranium fuel consists of small, " \
       "hard ceramic pellets that are packaged into long, vertical tubes. Bundles of this fuel are inserted into the " \
       "reactor. A single uranium pellet, slightly larger than a pencil eraser, contains the same energy as a ton of " \
       "coal, 3 barrels of oil, or 17,000 cubic feet of natural gas. Each uranium fuel pellet provides up to five " \
       "years of heat for power generation. And because uranium is one of the world's most abundant metals, " \
       "it can provide fuel for the world's commercial nuclear plants for generations to come. Nuclear power offers " \
       "many benefits for the environment as well. Power plants don't burn any materials so they produce no " \
       "combustion by-products. Additionally, because they don't produce greenhouse gases, nuclear plants help " \
       "protect air quality and mitigate climate change. When it comes to efficiency and reliability, " \
       "no other electricity source can match nuclear. Nuclear power plants can continuously generate large-scale, " \
       "around-the-clock electricity for many months at a time, without interruption. Currently, nuclear energy " \
       "supplies 12 percent of the world's electricity and approximately 20 percent of the energy in the United " \
       "States. As of 2018, a total of 30 countries worldwide are operating 450 nuclear reactors for electricity " \
       "generation. For decades, GE and Hitachi have been at the forefront of nuclear technology, setting the " \
       "industry benchmark for reactor design and construction and helping utility customers operate their plants " \
       "safely and reliably. "
print("--------------------\n", text, "\n-----------------------\n")

# =========================TEXT AND ARRAY FOMATTING=========================#

# format text and create array with each unique word
text = text.replace(".", "")
text = text.replace(",", "")
y = set(text.split(" "))
y = list(y)

# run genism keyword extraction and covert result into a list
x = keywords(text, words=100, scores=True, lemmatize=True)
x = list(x)

# converts each tuple genism returns into a list for future manipulation
gen = []
for i in x:
    i = list(i)
    gen.append(i)
print("GEN WEIGHTS------------------------\n", gen, "\n")


# =========================FUNCTIONS=========================#

# Weighted Sorting
# sort algorithm sorts the gen list by weight ascending
def indexedSort(array):
    l = len(array)
    for i in range(0, l):
        for j in range(0, l - i - 1):
            if array[j][1] > array[j + 1][1]:
                tempo = array[j]
                array[j] = array[j + 1]
                array[j + 1] = tempo
    return array


# =========================CUSTOM WEIGHT ALGORITHM=========================#

# empty list holds custom weight adjustments
wList = []
for w in y:
    freq = round(float(zipf_frequency(w, 'en')), 3)  # finds the frequency of each unique word in text
    wList.append([round((10 - freq) / 10, 2), w])  # adds the custom weight to wList
print("OUR WEIGHTS------------------------\n", wList, "\n")

# =========================HANDLING DUPLICATES AND PLURALS=========================#

tbd = []
for a in range(len(wList) - 1):
    for b in range(len(wList) - 1):
        print(a, b)
        if wList[a][1].lower() == wList[b][1].lower() and wList[a][1] != wList[b][
            1]:  # identifies duplicate words with different capitalization
            print("Same", wList[a][1], wList[b][1])
            wList[a][0] = (wList[a][0] + wList[b][0]) / 2  # average both duplicate weights
            tbd.append(wList[b][1])  # store name of word to be deleted
        if wList[a][1] in wList[b][1]:
            if wList[b][1] == wList[a][1] + "ing" or wList[b][1] == wList[a][
                1] + "s":  # identifies plural and verb forms of word
                print(wList[a][1], wList[b][1])

# loop through tbd and delete each word

# =========================WEIGHT ADJUSTMENT=========================#

# what constitutes a keyword?
# custom boost will hold the final boost we apply to genism weight
custom_boost = 0

added = []  # keeps track of what has been added
boosts = []  # keeps track of boosts applied to each word
for a in range(len(gen)):
    for b in range(len(wList)):
        if wList[b][1] in gen[a][0]:
            gen[a][1] += wList[b][
                             0] + custom_boost  # for each word in genism keyword, add our custom weight to the genism weight
            added.append(wList[b][1])
            # boosts.append(wList[b][1]) #debug purposes
            # boosts.append(wList[b][0]-(len(gen[a][0])/80)) #debug purposes
        else:
            if wList[b][1] not in added:  # if the word isn't in any list returned by genism, create a new entry
                gen.append([wList[b][1], wList[b][0] + custom_boost])
                added.append(wList[b][1])

print("NEW GEN-------------------------------\n", gen, "\n")

# =========================DEBUG=========================#

print(text.count("fission"))
for i in indexedSort(gen):
    print(i)

# =========================EXTRA/UNUSED CODE=========================#

# print(y)
# for t in y:
#     if (1 - round(float(word_frequency(t, 'en'))*10000, 3)) > 0:
#         numb = ((1 - round(float(word_frequency(t, 'en'))*10000, 3))+ x[c][1])/2
#         tList.append([numb, t])
#     c+=1

# print(sorted(tList))

# print(tList)

# from rake_nltk import Rake, Metric
# from collections import Counter
# r = Rake(max_length=3) # Uses stopwords for english from NLTK, and all puntuation characters.

# document='The function of this library is automatic summarization using a kind of natural language processing and
# neural network language model. This library enable you to create a summary with the major points of the original
# document or web-scraped text that filtered by text clustering. And this library applies pydbm to implement
# Encoder/Decoder based on LSTM (with an Attention mechanism) improving the accuracy of summarization by
# Sequence-to-Sequence(Seq2Seq) learning.'

# r.extract_keywords_from_text(document)

# # print(r.get_ranked_phrases_with_scores()) # To get keyword phrases ranked highest to lowest.

# print(Counter(document.split()).most_common())

# for i in range(len(r.get_ranked_phrases_with_scores())):
#     t=0
#     for w in r.get_ranked_phrases_with_scores()[i][1].split(" "):
#         t+=document.count(w)
#     print(t*r.get_ranked_phrases_with_scores()[i][0], r.get_ranked_phrases_with_scores()[i][1])
#     print(r.get_ranked_phrases_with_scores()[i][0], r.get_ranked_phrases_with_scores()[i][1])
#     print("-----------------------------------")


###########################################################################################

# from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
# from pysummarization.tokenizabledoc.simple_tokenizer import SimpleTokenizer
# from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor

# # Object of automatic summarization.
# auto_abstractor = AutoAbstractor()
# # Set tokenizer.
# auto_abstractor.tokenizable_doc = SimpleTokenizer()
# # Set delimiter for making a list of sentence.
# auto_abstractor.delimiter_list = [".", "\n"]
# # Object of abstracting and filtering document.
# abstractable_doc = TopNRankAbstractor()
# # Summarize document.
# result_dict = auto_abstractor.summarize(document, abstractable_doc)

# # Output result.
# for sentence in result_dict["summarize_result"]:
#     print(sentence)


############################################################################################

# Creates a text document of low weighed words to be avoided
# stopwords=""
# for p in range(len(wList)):
#     if wList[p][0]<0.4:
#         stopwords+=wList[p][1]+" "
# tf = open("stopwords.txt", "w")
# tf.write(stopwords)
# tf.close()

# Takes the higher weighted words and creates a seperate string with them to be run through genism again for a
# refined search

# document2 = ""
# for p in range(len(wList)):
#     if p > len(wList) / 2:
#         document2 += wList[p][1] + " "
# print(document2)
#
# print("----------------------------")
#
# from rake_nltk import Rake, Metric
# r = Rake("stopwords.txt", max_length=10)
# keywords1 = r.extract_keywords_from_sentences(text)
# keyphrases = r.get_ranked_phrases_with_scores
# keywords2 = r.extract_keywords_from_text(keyphrases[0][0])
# print(keywords1)
