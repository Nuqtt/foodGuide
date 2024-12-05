from flask import Flask, render_template
import urllib.request as request
import json

app = Flask(__name__)

src = "https://data.taipei/api/v1/dataset/f1df4d1b-7d3a-40c0-a40b-2bb359949862?scope=resourceAquire"


with request.urlopen(src) as response:
    data = json.loads(response.read().decode(encoding='utf-8'))

@app.route('/')
def index():
    return render_template('wc_list.html', data=data['result']['results'])

if __name__ == '__main__':
    app.run(debug=True)
