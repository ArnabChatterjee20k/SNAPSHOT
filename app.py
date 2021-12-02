from enum import unique
from os import name
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://N1ShN0BNrG:Em8XZ8mENE@remotemysql.com/N1ShN0BNrG"
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"

db=SQLAlchemy(app)

# MODELS
record = db.Table("mapping",
    db.Column("user_id",db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column("post_id",db.Integer, db.ForeignKey('post.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(10),unique=True,nullable = False)
    password = db.Column(db.String(20),nullable = False)
    user_ref = db.relationship('Post', secondary=record, lazy='dynamic',
        backref=db.backref('user'))

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(10),nullable = False)
    post = db.Column(db.LargeBinary,nullable = False)
    like_count = db.Column(db.Integer,nullable = True,server_default = "0")

@app.route('/')
def hello():
    return 'Hello World!'

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)