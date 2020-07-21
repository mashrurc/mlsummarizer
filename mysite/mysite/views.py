from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
@csrf_exempt
def index(request):
    return render(None, 'index.html')

# def backgroundProcess(request):
#     lang = request.args.get('proglang', 0, type = str)
#     print("---------------------")
#     print(lang) #prints the value from JS to output
#     print("---------------------")
#     # ml.document=lang #passes speech text to ml.py
#     # for sentence in ml.result_dict["summarize_result"]:
#     #     print(sentence)
#     #     print("AAA")
#     return 1
@csrf_exempt
def backgroundProcess(request):
   if request.method == 'GET':
       print("AAAAAAAAAAA")
   elif request.method == 'POST':
       ## access you data by playing around with the request.POST object
       print("AASDSA")
       print(request.POST.get('data'))
   return HttpResponse("Response")