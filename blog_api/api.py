from blog_api.constants import app, db
from blog_api.models import BlogPost

@app.get('/blogs')
def list_blogs():
    blogs = [{"id":blog.id, "title": blog.title, "subtitle": blog.subtitle, "body": blog.body, "created_at": blog.created_at} for blog in db.session.execute(db.select(BlogPost)).scalars()]
    return blogs
    
@app.post("/blogs")
def create_blog():
    return "blog post created"

@app.delete("/blogs/<int:blog_id>")
def test(blog_id):
    return f"deleted post {blog_id}"

@app.put("/blogs/<int:blog_id>")
def update_blog(blog_id):
    return f"update {blog_id}"


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