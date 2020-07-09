from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(None, 'index.html')

@app.route('/background_process')
def background_process():
    try:
        lang = request.args.get('proglang', 0, type = str)
        print("---------------------")
        print(lang) #prints the value from JS to output
        print("---------------------")
        t = processData(lang)
        # ml.document=lang #passes speech text to ml.py
        # for sentence in ml.result_dict["summarize_result"]:
        #     print(sentence)
        #     print("AAA")
        return jsonify(result=t)
    except Exception as e:
        return str(e)
