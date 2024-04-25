from blog_api.constants import app, db
from blog_api.models import BlogPost
from flask import request
from sqlalchemy import update


@app.get('/blogs')
def list_blogs():
    blogs = [{"id":blog.id, "title": blog.title, "subtitle": blog.subtitle, "body": blog.body, "created_at": blog.created_at} for blog in db.session.execute(db.select(BlogPost)).scalars()]
    return blogs

@app.get('/blogs/<int:blog_id>')
def get_blog(blog_id):
    res = db.get_or_404(BlogPost, blog_id)
    return {
        "title": res.title,
        "subtitle": res.subtitle, 
        "body": res.body,
        "created_at": res.created_at,
        "updated_at": res.updated_at
    }
    
@app.post("/blogs")
def create_blog():
    blog_details = request.get_json()
    try:
        new_blog = BlogPost(**blog_details)
        db.session.add(new_blog)
        db.session.commit()
        return {**blog_details, "id": new_blog.id, "created_at": new_blog.created_at}
    except Exception as e:
        print(e)
        return "Something went wrong"

@app.delete("/blogs/<int:blog_id>")
def test(blog_id):
    res = db.session.execute(BlogPost.__table__.delete().where(BlogPost.id==blog_id))
    db.session.commit()
    print(res)
    return f"deleted post {blog_id}"

@app.put("/blogs/<int:blog_id>")
def update_blog(blog_id):
    """
    Had some trouble with the returning method used here. Copying useful
    stackoverflow link for future reference.
    https://stackoverflow.com/questions/1049293/sqlite-error-cannot-commit-transaction-sql-statements-in-progress-using-java
    """
    updated = request.get_json()
    stmt = update(BlogPost.__table__).where(BlogPost.id==blog_id).values({key: value for key, value in updated.items() if key not in ("id", "created_at")}).returning(BlogPost.__table__.c.created_at, BlogPost.__table__.c.updated_at) 
    res = list(db.session.execute(stmt))
    #values of res have to be used before the commit or an error is thrown
    res = {**updated, "created_at": res[0].created_at, "updated_at": res[0].updated_at}
    db.session.commit()
    return res


@app.get("/blogs/seed")
def seed_db():
    for i in range(10):
        #the generated id is 1-indexed so this keeps the other info in line with the id
        id = i+1
        blog = BlogPost()
        blog.title = f"Title {id}"
        blog.subtitle = f"Subtitle {id}"
        blog.body = f"Body {id}"
        db.session.add(blog)
    db.session.commit()
    return "DB successfully seeded"