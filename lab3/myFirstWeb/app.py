from flask import Flask, render_template
import ubike

app = Flask(__name__, template_folder="../ubike/templates")

@app.route('/')
def index():
    data = ubike.get_data()
    return render_template('bike_list.html', data = data)

    
if __name__ == '__main__' : 
    app.run()