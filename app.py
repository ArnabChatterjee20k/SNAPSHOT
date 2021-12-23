from flask import Flask , render_template , session , request , url_for ,redirect
from flask_sqlalchemy import SQLAlchemy
import base64,time

# app configuration
app = Flask(__name__)
app.config['SECRET_KEY']='ikdfdhkfhkh394930248204fdjsljncaa'

# db configurations
db=SQLAlchemy(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://N1ShN0BNrG:Em8XZ8mENE@remotemysql.com/N1ShN0BNrG"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"


# custom filters fun and decorators and wrappers
@app.template_filter("b64_img")
def b64_img(img):
    """using custom filters of jinja for converting blob to image"""
    return base64.b64encode(img).decode("utf-8")

def custom_routing(function):
    def execute():
        if "user" in session:
            # print(session["user"])
            return function()
        else:
            return redirect(url_for("form"))
    return execute

def responsing(response,category,url=None):
    """a template to send a custom serializable response"""
    return {"response":response , "category" : category , "redirect_url": url }


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


# Endpoints for serving files.
@app.get('/')
def home():
    img_list = Post.query.all()
    return render_template("index.html",img_list = img_list)

@app.get("/post")
@custom_routing
def post():
    return render_template("post.html")

@app.get("/form")
def form():
    return render_template("form.html")

@app.get("/myprofile")
def profile():
    user = User.query.first()
    return render_template("profile.html")


# Only post endpoints. Acting as  REST api endpoints
@app.post("/submit")
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

@app.post("/register")
def reg():
    time.sleep(2)
    data =request.json
    try:
        name = data["name"]
        password = data["password"]
        url= url_for("home")
        check = User.query.filter_by(name=name).first()
        if check:
            return responsing(response=f"User {name} Exists",category="warning")
        else:
            data = User(name = name , password = password)
            db.session.add(data)
            db.session.commit()
            session["user"] = name
            return responsing(response=f"Thanks for registering",category="success",url=url)
    except:
        return responsing(response="Some error occured",category="warning")


@app.post("/log")
def log():
    time.sleep(2)
    data = request.json
    try:
        name = data["name"]
        password = data["password"]

        url= url_for("home")
        user = User.query.filter_by(name=name).first()
        if user:
            if user.password == password:
                session["user"] = name
                return responsing(response=f"User {name} Found",category="success",url=url)
            else:
                return responsing(response=f"Incorrect Password",category="warning",url=url)
        else:
            return responsing(response=f"User {name} Not Found",category="warning",url=url)
    
    except Exception as e:
        # print(e)
        return responsing(response="Some error occured",category="warning")

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(debug=True,host="0.0.0.0")#for running on all devices in the network.