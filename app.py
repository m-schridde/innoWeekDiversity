from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def indexByDefault():
    return index()

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/posts.html')
def posts():
    return render_template('posts.html')

if __name__ == "__main__":
    app.run(debug=True)
