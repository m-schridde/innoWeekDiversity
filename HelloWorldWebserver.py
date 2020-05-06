from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diversity.db'
db = SQLAlchemy(app)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Titel = db.Column(db.String(200), nullable=False)
    Text = db.Column(db.String(3000), nullable=False)
    Timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    MeTooCount = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Posts %r>' % self.id

class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200), nullable=False)
    ParentTag = db.Column(db.Integer)

    def __repr__(self):
        return '<Tags %r>' % self.id

class PostTagRelation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    PostId = db.Column(db.Integer)
    TagId = db.Column(db.Integer)
    WasAutomaticallyGenerated = db.Column(db.Integer, default = 1)

    def __repr__(self):
        return '<PostTagRelation %r>' % self.id

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        post_titel = request.form['titel']
        post_inhalt = request.form['inhalt']
        new_post = Posts(Titel = post_titel, Text = post_inhalt)
        
        try:
            db.session.add(new_post)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your Post'
    else:
        # return render_template('index.html')
        all_posts = Posts.query.order_by(Posts.Timestamp).all()
        all_tags = Tags.query.all()
        all_relations = PostTagRelation.query.all()
        return render_template('index.html', posts=all_posts, tags=all_tags, relations = all_relations)


@app.route('/deleteRelation/<int:id>')
def deleteRelation(id):
    relation_to_delete = PostTagRelation.query.get_or_404(id)

    try:
        db.session.delete(relation_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a Problem deleting that relation'


@app.route('/deletePost/<int:id>')
def deletePost(id):
    post_to_delete = Posts.query.get_or_404(id)

    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a Problem deleting that post'

@app.route('/incrementMeToo/<int:id>')
def incrementMeToo(id):
    post_to_increment = Posts.query.get_or_404(id)

    try:
        post_to_increment.MeTooCount = post_to_increment.MeTooCount + 1
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a Problem with incrementing me too count'

@app.route('/addTag', methods=['POST','GET'])
def addTag():
    if request.method == 'POST':
        tag_name = request.form['tagName']
        parent_Id = request.form['parentId']
        new_tag = Tags(Name = tag_name, ParentTag = parent_Id)

        try:
            db.session.add(new_tag)
            db.session.commit()
            return redirect('/')
        except:
                return 'There was an issue adding your Tag'
    else:
        return redirect('/') 

@app.route('/addRelation', methods=['POST','GET'])
def addRelation():
    if request.method == 'POST':
        post_id = request.form['postId']
        tag_id = request.form['tagId']
        new_relation = PostTagRelation(PostId = post_id, TagId=tag_id)

        try:
            db.session.add(new_relation)
            db.session.commit()
            return redirect('/')
        except:
                return 'There was an issue adding your Relation'
    else:
        return redirect('/')

@app.route('/deleteTag/<int:id>')
def deleteTag(id):
    tag_to_delete = Tags.query.get_or_404(id)

    try:
        db.session.delete(tag_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a Problem deleting that Tag'

if __name__ == "__main__":
    app.run(debug=True)
