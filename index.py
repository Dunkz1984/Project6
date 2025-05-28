from flask import Flask
from flask import render_template, request, redirect, url_for
import json, os
from datetime import datetime


app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'storage.json')

def read_json():
    try:
        print("Trying to read file:", DATA_FILE)
        print("File exists:", os.path.exists(DATA_FILE))
        
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
            return data
            
    except FileNotFoundError: #This is not my creation, but allows for errors to be found.
        print("File not found!")
        return {"posts": []}
    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
        return {"posts": []}

def write_json(data):
     os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
     with open(DATA_FILE, 'w') as file:
          json.dump(data, file, indent=2)

@app.context_processor #This allows for the old blogs to basically always be on the side of the page
def oldblog():
     data = read_json()
     posts = data.get('posts', [])
     return {'posts': posts}
     
    
@app.route("/")
def home():
    data = read_json()
    posts = data.get('posts', [])

    if posts:
        latest_post = posts[-1]
        return render_template('home.html', post=latest_post)
    else:
        return render_template('home.html', post=None)

@app.route("/about")
def about():
    return render_template('about.html')
      

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        data = read_json()
    
        new_post = {
            'id': len(data['posts']) + 1,
            'title' : title,
            'content' : content,
            'date' : datetime.now().strftime("%d/%m/%Y")
        }

        data['posts'].append(new_post)

        write_json(data)

        return redirect(url_for('home'))

    

    data = read_json()
    posts = data.get('posts', [])
     
    return render_template("create.html", posts=posts)

if __name__ == "__main__":
    app.run(debug=True)