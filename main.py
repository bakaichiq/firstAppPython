from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
                                   
    def __init__(self, name):
        self.name = name

class AuthorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


author_schema = AuthorSchema(many=True)
authors_schema = AuthorSchema(many=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(21), unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))

    def __init__(self, title):
        self.title = title

class PostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'author_id')

post_schema = PostSchema()
posts_schema = PostSchema(many=True) #  Don't forget to initiate the class


#Авторы
@app.route('/author', methods=['POST'])
def add_author():
    data = request.json()
    new_author = Author(data.get('name'))
    db.session.add(new_author)
    db.session.commit()

    return author_schema.jsonify(new_author)

@app.route('/author', methods=['GET'])
def get_author():
    all_authors = Author.query.all()
    result = authors_schema.dump(all_authors)
    return jsonify(result)

@app.route('/author/<id>', methods=['GET'])
def get_author1(id):
    author = Author.query.get(id)
    return author_schema.json(author)


#Update author

@app.route('/author/<id>', methods=['PUT'])
def update_author(id):
    author = Author.query.get(id)
    name = request.json('name')
    author.name = name

    db.session.commit()

    return author_schema.jsonify(author)


# Посты
@app.route('/post', methods=['POST'])
def add_post():
    data = request.json
    new_post = Post(data.get('title', 'author_id'))
    db.session.add(new_post)
    db.session.commit()

    return post_schema.jsonify(new_post)

@app.route('/post', methods=['GET'])
def get_post():
    all_posts = Post.query.all()
    result = posts_schema.dump(all_posts)
    return jsonify(result)
#
# @app.route('/post/<id>', methods=['GET'])
# def get_post():
#     post = Post.query.get(id)
#     return post_schema.jsonify(post)

if __name__ == '__main__':
   app.run(debug=True)