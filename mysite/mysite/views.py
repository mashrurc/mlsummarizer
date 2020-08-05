from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from wordfreq import zipf_frequency, word_frequency
from gensim.summarization import keywords, summarize
from textwrap import wrap
from fpdf import FPDF
import json
import wikipedia
import pdfkit


@csrf_exempt
def index(request):
    return render(None, 'index.html')


@csrf_exempt
def backgroundProcess(request):
   returning = ""
   if request.method == 'GET':
       print("AAAAAAAAAAA")
   elif request.method == 'POST':
        print(request.POST.get('data'))
        x = request.POST.get('data')
        text = x
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
       "safely and reliably."
        s = summarize(text)
        summarized = s.replace("\n", "  ")
        wraped_text = "\n".join(wrap(summarized, 80))
        print("--------------------\n", text, "\n-----------------------\n")

        # =========================TEXT AND ARRAY FOMATTING=========================#

        # format text and create array with each unique word
        text = text.replace(".", "")
        text = text.replace(",", "")
        y = set(text.split(" "))
        y = list(y)
        print(y)

        # run genism keyword extraction and covert result into a list
        x = keywords(text, words=100, scores=True, lemmatize=True)
        x = list(x)

        # converts each tuple genism returns into a list for future manipulation
        gen = []
        for i in x:
            i = list(i)
            gen.append(i)

        for i in range(len(gen)):
            temp = gen[i][0]
            gen[i][0] = gen[i][1]
            gen[i][1] = temp

        print("\nGEN WEIGHTS------------------------\n", gen, "\n")


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

        final = []
        def finalList(l):
            for items in l:
                final.append(items[1])
            return final


        def pluralRemove(arr):
            tbd = []
            for a in range(len(sorted(arr)) - 1):
                for b in range(len(sorted(arr)) - 1):
                    if arr[a][1].lower() == arr[b][1].lower() and arr[a][1] != arr[b][1]:  # identifies duplicate words with different capitalization
                        if arr[b][1].lower() not in tbd:
                            print("Same", arr[a][1], arr[a][0], "and", arr[b][1], arr[b][0])  # average both duplicate weights
                            arr[b][0] = (arr[a][0] + arr[b][0]) / 2
                            print("adjusted", arr[b][0])
                            tbd.append(arr[b][1].lower())  # store name of word to be deleted
                    if arr[a][1] in arr[b][1]:
                        if arr[b][1] == arr[a][1] + "ing" or arr[b][1] == arr[a][1] + "s" or arr[b][1] == arr[a][1] + "r" or \
                                arr[b][1] == arr[a][1] + "er" or arr[b][1] == arr[a][1] + "est" and len(arr[a][1]) > 1 and len(arr[b][1]) > 1:  # identifies plural and verb forms of word
                            if arr[b][1].lower() not in tbd:
                                print("plural-ing", arr[a][1], arr[a][0], "and", arr[b][1], arr[b][0])
                                arr[a][0] = (arr[a][0] + arr[b][0]) / 2
                                print("adjusted", arr[a][0])
                                tbd.append(arr[b][1].lower())

            print(tbd)
            t = 0
            for deleted in tbd:
                for a in arr:
                    if deleted == a[1]:
                        del arr[t]
                        t -= 1
                    t += 1
                t = 0

        def avgWeight(arr):
            count=0
            for i in arr:
                count+=i[0]
            avg=count/len(arr)
            print("AVERAGE OF GEN", avg)

        # =========================CUSTOM WEIGHT ALGORITHM=========================#

        # empty list holds custom weight adjustments
        wList = []
        for w in y:
            freq = round(float(zipf_frequency(w, 'en')), 3)  # finds the frequency of each unique word in text
            wList.append([(9.5 - freq) / 5, w])  # adds the custom weight to wList
        print("\nOUR WEIGHTS------------------------\n", wList, "\n")

        # =========================HANDLING DUPLICATES AND PLURALS=========================#

        pluralRemove(wList)

        for w in wList:
            gen.append([w[0], w[1]])

        pluralRemove(gen)

        # =========================WEIGHT ADJUSTMENT=========================#

        # what constitutes a keyword?
        # custom boost will hold the final boost we apply to genism weight

        added = []  # keeps track of what has been added
        boosts = []  # keeps track of boosts applied to each word

        added = []
        for i in range(len(gen)):
            # for word in gen[i][0].split(" "):
            for a in wList:
                if a[1].lower() in gen[i][1].split(" "):
                    custom_boost = a[0]
                    #print("adding", gen[i][0],":",gen[i][1], a[1],":",a[0])
                    gen[i][0] += custom_boost
                    # print("result", gen[i][1])
                    if a[1] not in added:
                        added.append(a[1])

        # =========================AVERAGE REMOVAL=========================#

        avgWeight(gen)

        # =========================DEBUG=========================#
        definitions = []
        count = 0
        print("FINAL WEIGHT RANKINGS WLIST-------------------------------------\n")
        for i in sorted(wList,reverse=True):
            print(i)
            if count <= int(len(wList)/14):
                try:
                    definitions.append((i[1], wikipedia.summary(i[1], sentences=1)))
                except:
                    print("error")
                    count-=1
            if count > int(len(wList)/9):
                print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", count)
                break
            # returning += i[1] +" "
            count+=1
    
        print("Definitions------------------------------------\n")
        print(definitions)
        for x in definitions:
            returning += x[0]+ " : "+x[1]+"\n\n"

        print("FINAL WEIGHT RANKINGS GEN------------------------------------\n")
        for i in sorted(gen, reverse=True):
            print(i)
        
        print(returning)
        
        finalreturn = summarized + "\n\n" +returning
        
            
      
   return HttpResponse(finalreturn)
# =========================IMPORTS=========================#

# import word frequency and keyword extraction libraries

