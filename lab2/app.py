
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    names = {'name': 'Rebecca'}
    items = [{'text':'First'},{'text':'Second'},{'text':'Third'}]
    return render_template("layout.html", names=names, items=items, language="Python", lang=True, framework="Flask")

if __name__ == '__main__':
    app.run()