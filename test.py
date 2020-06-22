from flask import Flask, request, send_from_directory, render_template

# set the project root directory as the static folder, you can set others.
app = Flask(__name__,
            static_url_path='/static')

# @app.route('/js/<path:path>')
# def send_js(path):
#     return send_from_directory('js', path)

@app.route('/')
def index():
    return render_template("index.html")

# @app.route('/my-link/', methods=['POST'])
# def myLink():
#     return request.form['projectFilePath']

if __name__ == "__main__":
    app.run()
