from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS 
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True) # unique id primary key column creation
    title = db.Column(db.String, nullable=False)
    artist = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    review = db.Column(db.String, nullable=False)

    def __init__(self, title, artist, genre, review):
        self.title = title
        self.artist = artist
        self.genre = genre
        self.review = review

class BlogPostSchema(ma.Schema):
    class Meta:
        fields = ('id','title', 'artist', 'genre', 'review')

blog_post_schema = BlogPostSchema()
blog_posts_schema = BlogPostSchema(many=True)



# Endpoint to create a new blog post
@app.route('/blog', methods=["POST"])
def add_blog():
    title = request.json['title']
    artist = request.json['artist']
    genre = request.json['genre']
    review = request.json['review']

    new_blog = BlogPost(title, artist, genre, review)
    db.session.add(new_blog)
    db.session.commit()

    blog_post = BlogPost.query.get(new_blog.id)

    return blog_post_schema.jsonify(blog_post)


# Endpoint to query all blog posts
@app.route("/blogs", methods=["GET"])
def get_blogs():
    all_blogs = BlogPost.query.all()
    result = blog_posts_schema.dump(all_blogs)
    return jsonify(result)


# Endpoint for single blog
@app.route("/blog/<id>", methods=["GET"])
def get_blog(id):
    blog = BlogPost.query.get(id)
    return blog_post_schema.jsonify(blog)


# Endpoint for deleting a record
@app.route("/blog/<id>", methods=["DELETE"])
def remove_blog(id):
    blog = BlogPost.query.get(id)
    db.session.delete(blog)
    db.session.commit()

    return blog_post_schema.jsonify(blog)

if __name__ == '__main__':
    app.run(debug=True)