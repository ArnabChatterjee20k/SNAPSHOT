import io
from logging import exception
import pstats
from webbrowser import get
from flask import Flask, abort , render_template , session , request , url_for ,redirect
from flask_sqlalchemy import SQLAlchemy
import base64 , os
from faker import Faker
from PIL import Image
from flask_migrate import Migrate
# app configuration
app = Flask(__name__)
app.config['SECRET_KEY']='ikdfdhkfhkh394930248204fdjsljncaa'
faker = Faker()

# db configurations
db=SQLAlchemy(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://N1ShN0BNrG:Em8XZ8mENE@remotemysql.com/N1ShN0BNrG"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"

# migration
migrate = Migrate(app=app , db=db)

# custom filters fun and decorators and wrappers
@app.template_filter("b64_img")
def b64_img(img):
    """using custom filters of jinja for converting blob to image"""
    return base64.b64encode(img).decode("utf-8")

def custom_routing(function):
    "a decorator for managing sessions"
    def execute(**kwargs):
        if "user" in session:
            return function()
        else:
            return redirect(url_for("form"))
    execute.__name__ = function.__name__
    return execute

def responsing(response,category,url=None):
    """a template to send a custom serializable response"""
    return {"response":response , "category" : category , "redirect_url": url }

def image_compressor(image):
    # TODO: to compress images to specific dimension
    """ 
        If height and width are greater than 640 then compress
    """
    image_read_from_byte = Image.open(io.BytesIO(image))
    width , height = image_read_from_byte.size

    if height > 500 or width>500:
        output_size = (500,500)
        image_read_from_byte.thumbnail(output_size)

        stream = io.BytesIO()
        image_read_from_byte.save(stream , "PNG")

        return stream.getvalue()
    return image
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(10),unique=True,nullable = False)
    password = db.Column(db.String(20),nullable = False)
    post_name = db.relationship('Post',lazy="dynamic",backref=db.backref("author"))
    like_id = db.relationship('Likes',lazy="dynamic",backref=db.backref("author"))
    
class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(10),nullable = False)
    post = db.Column(db.LargeBinary,nullable = False)
    # like_count = db.Column(db.Integer,nullable = True,server_default = "0")
    user_id = db.Column(db.Integer , db.ForeignKey("user.id"),nullable = False )#name of the user who will be posting
    like_id = db.relationship('Likes',lazy="dynamic",backref=db.backref("post"))

class Likes(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer , db.ForeignKey("user.id"))
    post_id = db.Column(db.Integer , db.ForeignKey("post.id"))
# Endpoints for serving files.
@app.get('/')
def home():
    img_list = Post.query.all()
    user_id = None        
    if session.get("user"):
        user_id = User.query.filter_by(name=session.get("user")).first().id
    return render_template("index.html",img_list = img_list , user_id=user_id,Like=Likes)

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
@custom_routing
def my_profile():
    user_name = session.get("user")
    user = User.query.filter_by(name=user_name).first()
    # img_list = Post.query.filter_by(author = user)
    img_list = user.post_name
    return render_template("profile.html",img_list=img_list)

@app.get("/userprofile/<int:id>")
def user_profile(id):
    user = User.query.get_or_404(id)
    # img_list = Post.query.filter_by(author = user)
    img_list = user.post_name # as we are having post_name as the relation column
    return render_template("profile.html",img_list=img_list,user_name=user.name)
# Only post endpoints. Acting as  REST api endpoints
@app.post("/submit")
def submit():
        name = session.get("user")

        """requeat.file will give File storage object. We need to tranform it to bytes like this:-"""
        file = request.files.get("file")
        post_name = request.form.get("name")
        # print(file)#we will see it is a FIlestorage object
        image_file_data_bytes = file.read()
        compressed_image_file_data_bytes = image_compressor(image_file_data_bytes)

        user = User.query.filter_by(name=name).first()
        post = Post(name=post_name,post=compressed_image_file_data_bytes,author = user)
        
        try:
            db.session.add(post)
            db.session.commit()
            return {"redirect_url" : url_for("home")}
        except Exception as e:
            print(e)
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

@app.get("/likes/<int:post_id>")
def likes(post_id):
    # we will get the userid from the session user
    if not session.get("user"):
        return {"status":"please login","url":"/form"}
    username = session.get("user")
    user = User.query.filter_by(name=username).first()
    post = Post.query.get(post_id)
    like = Likes.query.filter_by(user_id= user.id, post_id=post_id).first() # using backref post
    if not post:
        return abort(404)
    elif like:
        try:
            db.session.delete(like)
            db.session.commit()
            return {"status":"disliked"}
        except Exception as e:
            print(e)
            return {"status":"error"}
    else:
        new_like = Likes(user_id=user.id , post_id=post_id )
        db.session.add(new_like)
        db.session.commit()
        return {"status":"liked"}
if __name__ == '__main__':
    if not os.path.exists("/test.db"):
        db.create_all()
    app.run(debug=True,host="0.0.0.0")#for running on all devices in the network.