from flask import Flask , render_template , session , request , url_for ,redirect
from flask_sqlalchemy import SQLAlchemy
import base64 , os
from faker import Faker
# app configuration
app = Flask(__name__)
app.config['SECRET_KEY']='ikdfdhkfhkh394930248204fdjsljncaa'
faker = Faker()

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
    "a decorator for managing sessions"
    def execute():
        if "user" in session:
            return function()
        else:
            return redirect(url_for("form"))
    execute.__name__ = function.__name__
    return execute

def responsing(response,category,url=None):
    """a template to send a custom serializable response"""
    return {"response":response , "category" : category , "redirect_url": url }

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(10),unique=True,nullable = False)
    password = db.Column(db.String(20),nullable = False)
    post_name = db.relationship('Post',lazy="dynamic",backref=db.backref("author"))
    
class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(10),nullable = False)
    post = db.Column(db.LargeBinary,nullable = False)
    like_count = db.Column(db.Integer,nullable = True,server_default = "0")
    user_id = db.Column(db.String(100) , db.ForeignKey("user.id"),nullable = False )#name of the user who will be posting


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
    name = faker.name()
    password = faker.password()
    return render_template("form.html",name=name,password=password)

@app.get("/myprofile")
# @custom_routing
def profile():
    return render_template("profile.html")


# Only post endpoints. Acting as  REST api endpoints
@app.post("/submit")
def submit():
        name = session.get("user")

        """requeat.file will give File storage object. We need to tranform it to bytes like this:-"""
        file = request.files.get("file")
        print(file)#we will see it is a FIlestorage object
        file_data_bytes = file.read()
        
        user = User.query.filter_by(name=name).first()
        post = Post(name=file.filename,post=file_data_bytes,author = user)
        
        try:
            db.session.add(post)
            db.session.commit()
            return {"redirect_url" : url_for("home")}
        except:
            return {"message":"Some problem occured"}

@app.post("/register")
def reg():
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
    data = request.json
    try:
        name = data["name"]
        password = data["password"]

        url = url_for("home") 
        user = User.query.filter_by(name=name).first()
        if user:
            if user.password == password:
                session["user"] = name
                return responsing(response=f"User {name} Found",category="success",url=url)
            else:
                return responsing(response=f"Incorrect Password",category="warning")
        else:
            return responsing(response=f"User {name} Not Found",category="warning")
    
    except Exception as e:
        # print(e)
        return responsing(response="Some error occured",category="warning")

if __name__ == '__main__':
    if not os.path.exists("/test.db"):
        db.create_all()
    app.run(debug=True,host="0.0.0.0")#for running on all devices in the network.