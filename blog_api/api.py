from blog_api.constants import app, db, login_manager
from blog_api.models import BlogPost, User
from flask import request, render_template, redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user
from sqlalchemy import update, and_
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, TextAreaField
import random
import secrets

class BlogForm(FlaskForm):
    title = StringField("Title")
    subtitle = StringField("Subtitle")
    body = TextAreaField("Body")
    submit = SubmitField("Save Changes")

class LoginForm(FlaskForm):
    username = StringField("Username")
    password = StringField("Password")
    submit = SubmitField("Login")

class SignupForm(FlaskForm):
    username = StringField("Username")
    password = StringField("Password")
    password_repeat = StringField("Confirm password")
    submit = SubmitField("Sign up")

@app.get('/')
def list_blogs():
    blogs = [{"id":blog.id, "title": blog.title, "subtitle": blog.subtitle, "body": blog.body, "created_at": blog.created_at, "author": blog.author.username} for blog in db.session.execute(db.select(BlogPost)).scalars()]
    if len(blogs)==0:
        seed_db()
        blogs = [{"id":blog.id, "title": blog.title, "subtitle": blog.subtitle, "body": blog.body, "created_at": blog.created_at, "author": blog.author.username} for blog in db.session.execute(db.select(BlogPost)).scalars()]
    return render_template('./blogs.html', blogs=blogs)

@app.get("/blogs/create")
def new_blog_form():
    form = BlogForm()
    return render_template("new_blog.html", form=form)

@app.get('/blogs/<int:blog_id>')
def get_blog(blog_id):
    res = db.get_or_404(BlogPost, blog_id)
    blog = {
        "id": res.id,
        "title": res.title,
        "subtitle": res.subtitle, 
        "body": res.body,
        "created_at": res.created_at,
        "updated_at": res.updated_at,
        "author": res.author.username
    }
    return render_template('./blog.html', blog=blog, is_authed=(current_user.is_authenticated and current_user.id==res.author.id))
    
@app.post("/blogs/create")
@login_required
def create_blog():
    blog_details = request.form
    try:
        new_blog = BlogPost(title=blog_details["title"], subtitle=blog_details["subtitle"], body=blog_details["body"],  author_id=int(current_user.id))
        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for("get_blog", blog_id=new_blog.id))
    except Exception as e:
        print(e)
        return "Something went wrong"

@app.get("/blogs/<int:blog_id>/delete")
@login_required
def delete_blog(blog_id):
    res = db.session.execute(BlogPost.__table__.delete().where(and_(BlogPost.id==blog_id, BlogPost.author_id==int(current_user.id))))
    db.session.commit()
    return redirect(url_for("list_blogs"))

@app.get("/blogs/<int:blog_id>/edit")
@login_required
def edit_blog_form(blog_id):
    to_update = db.get_or_404(BlogPost, blog_id)
    form = BlogForm(obj=to_update)
    return render_template("./edit_blog.html", form=form, blog_id=to_update.id)

@app.post("/blogs/<int:blog_id>/edit")
@login_required
def update_blog(blog_id):
    """
    Had some trouble with the returning method used here. Copying useful
    stackoverflow link for future reference.
    https://stackoverflow.com/questions/1049293/sqlite-error-cannot-commit-transaction-sql-statements-in-progress-using-java
    """
    #BUG: Potential bug, if only provide one field, only that field+created_at & updated_at are returned
    updated = request.form
    print(f"Updated {updated}")
    stmt = update(BlogPost.__table__).where(and_(BlogPost.id==blog_id, BlogPost.author_id==int(current_user.id))).values({key: value for key, value in updated.items() if key in ("title", "subtitle", "body")})
    res = db.session.execute(stmt)
    db.session.commit()
    return redirect(url_for("get_blog", blog_id=blog_id))


@app.post("/signup")
def signup():
    user_info = request.get_json()
    new_user = User(**user_info)
    db.session.add(new_user)
    db.session.commit()
    return {"username": user_info["username"], "id": new_user.id}

@app.get("/login")
def get_login():
    form = LoginForm()
    return render_template("./login.html", form=form)

@app.post("/login")
def login():
    username, password, submit = request.form.values()
    user = User.query.filter(and_(User.username==username, User.password==password)).first()
    if(user):
        #redirect to main page
        login_user(user, force=True)
        return redirect(url_for("get_profile", user_id=user.id))
    return redirect(url_for( 'get_login', retry=True))

@app.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("list_blogs"))

@app.get("/sign-up")
def sign_up_page():
    form = SignupForm()
    return render_template("./sign-up.html", form=form)

@app.post("/sign-up")
def sign_up():
    form = request.form
    new_user = User(username=form["username"], password=form["password"])
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("get_login"))


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id==int(user_id)).one()


@app.get("/profile/<int:user_id>")
@login_required
def get_profile(user_id):
    blogs = [{"id":blog.id, "title": blog.title, "subtitle": blog.subtitle, "body": blog.body, "created_at": blog.created_at, "author": blog.author.username} for blog in db.session.execute(db.select(BlogPost).filter(BlogPost.author_id==user_id)).scalars()]
    return render_template("./profile.html", blogs=blogs)

@app.get("/authstatus")
def get_auth_status():
    return {
        "current_user": None if current_user.is_anonymous else current_user.username
    }


def seed_db():
    #only create 2 users for simplicity
    users = []
    for i in range(2):
        user_num = i+1
        username = f"user{user_num}"
        password = f"password{user_num}"
        users.append(User(username=username, password=password))
    db.session.add_all(users)
    db.session.commit()
        
    for i in range(10):
        #the generated id is 1-indexed so this keeps the other info in line with the id
        id = i+1
        blog = BlogPost()
        blog.title = f"Title {id}"
        blog.subtitle = f"Subtitle {id}"
        blog.body = f"Body {id}"
        blog.author_id = users[0].id if i<5 else users[1].id
        db.session.add(blog)
    db.session.commit()
    return "DB successfully seeded"