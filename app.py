from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from mockKi import mockKi
from Model_for_Backend_New.predict_category import predict_category
from sqlalchemy import desc

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

@app.route('/')
def indexByDefault():
    return index()

@app.route('/index.html')
def index():
    #all_posts = Posts.query.order_by(desc(Posts.Timestamp)).all()
    return render_template('index.html')

@app.route('/addPost', methods=['POST','GET'])
def addPost():
    if request.method == 'POST':
        post_titel = request.form['input-title']
        post_inhalt = request.form['input-message']
        new_post = Posts(Titel = post_titel, Text = post_inhalt)
        proposed_tags = predict_category(post_inhalt)
        try:
            db.session.add(new_post)
            db.session.commit()
        except:
            return 'There was an issue adding your Post'
        post_id = new_post.id
        for tag_name in proposed_tags:
            tags_by_name = Tags.query.filter_by(Name = tag_name)
            if tags_by_name.count() == 0:
                addTag(tag_name)

            this_tag = Tags.query.filter_by(Name = tag_name).first()
            tag_id = this_tag.id


            new_relation = PostTagRelation(PostId = post_id, TagId=tag_id)
            try:
                db.session.add(new_relation)
                db.session.commit()
            except:
                return "huge fuckup"

        all_tags = Tags.query.all()
        all_relations = PostTagRelation.query.all()
        return render_template('confirm.html', post = new_post, tags=all_tags, relations=all_relations)        
    else:
        return render_template('index.html')

# @app.route('/confirmPost/<int:id>')
# def confirmPost(id):
#     post_to_be_confirmed = Posts.query.get_or_404(id)
    


@app.route('/posts.html')
def posts():
    all_posts = Posts.query.order_by(desc(Posts.Timestamp)).all()
    all_tags = Tags.query.all()
    all_relations = PostTagRelation.query.all()
    return render_template('posts.html', posts=all_posts, tags=all_tags, relations=all_relations)

@app.route('/incrementMeToo/<int:id>')
def incrementMeToo(id):
    post_to_increment = Posts.query.get_or_404(id)

    try:
        post_to_increment.MeTooCount = post_to_increment.MeTooCount + 1
        db.session.commit()
        return redirect('/posts.html#post%s' % id)
    except:
        return 'There was a Problem with incrementing me too count'

@app.route('/deletePost/<int:id>')
def deletePost(id):
    post_to_delete = Posts.query.get_or_404(id)
    relation_to_delete =  PostTagRelation.query.filter_by(PostId = post_to_delete.id).first()
    while isinstance(relation_to_delete, PostTagRelation):
        try:
            db.session.delete(relation_to_delete)
            db.session.commit()
        except:
            return 'There was a Problem deleting that post'
        relation_to_delete =  PostTagRelation.query.filter_by(PostId = post_to_delete.id).first()
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a Problem deleting that post'

@app.route('/addRelation/<int:id>', methods=['POST','GET'])
def addRelation(id):
    if request.method == 'POST':
        tag_name = request.form['tagName']
        tags_by_name = Tags.query.filter_by(Name = tag_name)
        if tags_by_name.count() == 0:
            addTag(tag_name)

        this_tag = Tags.query.filter_by(Name = tag_name).first()
        tag_id = this_tag.id


        new_relation = PostTagRelation(PostId = id, TagId=tag_id)


        try:
            db.session.add(new_relation)
            db.session.commit()
            current_post = Posts.query.get_or_404(id)
            all_tags = Tags.query.all()
            all_relations = PostTagRelation.query.all()
            return render_template('confirm.html', post = current_post, tags=all_tags, relations=all_relations)
        except:
                return 'There was an issue adding your Relation'
    else:
        return redirect('/')
def addTag(name):
    #tag_name = request.form['tagName']
    #parent_Id = request.form['parentId']
    new_tag = Tags(Name = name, ParentTag = 1)

    try:
        db.session.add(new_tag)
        db.session.commit()
    except:
        print('There was an issue adding your Tag')
    

@app.route('/deleteRelation/<int:id>')
def deleteRelation(id):
    relation_to_delete = PostTagRelation.query.get_or_404(id)
    post_id = relation_to_delete.PostId
    current_post = Posts.query.get_or_404(post_id)

    try:
        db.session.delete(relation_to_delete)
        db.session.commit()
        all_tags = Tags.query.all()
        all_relations = PostTagRelation.query.all()
        return render_template('confirm.html', post = current_post, tags=all_tags, relations=all_relations)
    except:
        return 'There was a Problem deleting that relation'


@app.route('/statistics.html')
def statistics():

            tag_id_relations = PostTagRelation.query.all()
            tags = Tags.query.all()
            tags_sum = PostTagRelation.query.count()
            all_tags_count = {}
            
            for tag in tags:

                tag_id = tag.id
                tag_count = PostTagRelation.query.filter_by(TagId = tag_id).count()
                all_tags_count[tag] = round(((tag_count / tags_sum) * 100), 1)

            return render_template('statistics.html', tags = all_tags_count)


@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/searchByTag', methods=['POST','GET'])
def searchByTag():
    tag_name = request.form['input-search-tag']
    try: 
        this_tag = Tags.query.filter_by(Name = tag_name).first()
        tag_id = this_tag.id
        post_tag_relations = PostTagRelation.query.filter_by(TagId = tag_id).all()
        related_posts = []
        for relation in post_tag_relations:
            related_posts.append(Posts.query.filter_by(id = relation.PostId).first())
        return render_template('posts.html', posts = related_posts)
    except:
        return posts()

if __name__ == "__main__":
    app.run(debug=True)
