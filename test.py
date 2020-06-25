from flask import Flask, request, send_from_directory, render_template, jsonify
from gensim.summarization import keywords
# from ml import processData
lecture=""

# set the project root directory as the static folder, you can set others.
app = Flask(__name__,
            static_url_path='/static')

# @app.route('/js/<path:path>')
# def send_js(path):
#     return send_from_directory('js', path)
def processData(theData):
    text = theData
    x = keywords(text).split('\n')
    return x

@app.route('/')
def index():
    return render_template("index.html")

# @app.route('/my-link/', methods=['POST'])
# def myLink():
#     return request.form['projectFilePath']

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

if __name__ == "__main__":
    app.run()
