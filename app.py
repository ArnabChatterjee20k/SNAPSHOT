from flask import Flask , render_template , session , request
from flask_sqlalchemy import SQLAlchemy
import base64
app = Flask(__name__)

#using custom filters of jinja for converting blob to image
@app.template_filter("b64_img")
def b64_img(img):
    return base64.b64encode(img).decode("utf-8")
    
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://N1ShN0BNrG:Em8XZ8mENE@remotemysql.com/N1ShN0BNrG"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"

db=SQLAlchemy(app)

# MODELS
# this table is for mapping likes to post. If any user like the post then only things will be added.
record = db.Table("mapping",
    db.Column("user_id",db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column("post_id",db.Integer, db.ForeignKey('post.id'), primary_key=True)
)
#Rather I can do I can keep one one rln between users and their posts. Bcoz one post can have one user but an user can have many post. This if for keeping post. Post table is having like column default to none.
#And I can make many many to relation between users and the post they liked. I have to use the record table for keeping user name and post they are liking. Now while liking if user has not liked the post then we will do +1 to the like column in Post. Else if already liked we will not do +1.

#One to many between user and post.
#Many to many between 
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(10),unique=True,nullable = False)
    password = db.Column(db.String(20),nullable = False)
    user_like_post = db.relationship('Post', secondary=record, lazy='dynamic',
        backref=db.backref('user'))

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(10),nullable = False)
    post = db.Column(db.LargeBinary,nullable = False)
    like_count = db.Column(db.Integer,nullable = True,server_default = "0")
    user_name = db.Column(db.String(100) , nullable = False )#name of the user who will be posting

@app.route('/')
def hello():
    img_list = Post.query.all()
    return render_template("index.html",img_list = img_list)

@app.route("/post")
def post():
    return render_template("post.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/submit",methods=['POST'])
def submit():
        name = request.form.get("name")

        """requeat.file will give File storage object. We need to tranform it to bytes like this:-"""
        file = request.files.get("file")
        print(file)#we will see it is a FIlestorage object
        file_data_bytes = file.read()
        
        post = Post(name=name,post=file_data_bytes,user_name = "arnab")
        db.session.add(post)
        db.session.commit()        
        
        db.session.add(post)
        db.session.commit()
        return {"name":name,"file":file.filename}

@app.route("/login",methods=['POST'])
def log():
    # print(request.json)
    return "Thanks for registering"
if __name__ == '__main__':
    # app.run(debug=True)
    app.run(debug=True,host="0.0.0.0")#for running on all devices in the network.