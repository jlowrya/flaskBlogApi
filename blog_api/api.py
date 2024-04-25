from blog_api.constants import app

@app.get('/blogs')
def list_blogs():
    return "look at all these blog posts"
    
@app.post("/blogs")
def create_blog():
    return "blog post created"

@app.delete("/blogs/<int:blog_id>")
def test(blog_id):
    return f"deleted post {blog_id}"

@app.put("/blogs/<int:blog_id>")
def update_blog(blog_id):
    return f"update {blog_id}"

