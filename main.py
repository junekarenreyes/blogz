from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '11111'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(120))
    body = db.Column(db.Text)

    def __init__(self, blog_title, body):
        self.blog_title = blog_title
        self.body = body

#You're able to submit a new post at the /newpost route. 
#After submitting a new post, your app displays the main blog page.
@app.route("/newpost", methods=['POST', 'GET'])
def postblog():
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        body = request.form['body']
        blog_post = Blog(blog_title, body)
        db.session.add(blog_post)
        db.session.commit()
        return redirect('/')

    return render_template('newpost.html', title="Add a Blog Entry")


@app.route("/", methods=['GET'])
def index():
    blogged = Blog.query.filter(Blog.body != None).all()
    return render_template('blog.html', title="Build a Blog!", blogged=blogged)

#The /blog route displays all the blog posts.
#@app.route("/blog", methods=['GET'])


if __name__ == '__main__':
    app.run()