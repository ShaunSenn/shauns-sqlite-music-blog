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