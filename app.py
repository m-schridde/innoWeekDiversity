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

@app.route('/statistics.html')
def statistics():
    return render_template('statistics.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
