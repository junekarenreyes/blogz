from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

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
    pub_date = db.Column(db.DateTime)

    def __init__(self, blog_title, body, pub_date=None):
        self.blog_title = blog_title
        self.body = body
        if pub_date is None:
            pub_date = datetime.now(pytz.timezone('US/Pacific'))
        self.pub_date = pub_date
    
    def __repr__(self):
        return '<Blog %r>' % self.blog_title

#You're able to submit a new post at the /newpost route. 
#After submitting a new post, your app displays the main blog page.
@app.route("/newpost", methods=['POST', 'GET'])
def postblog():
    blog_title = ""
    body = ""

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        body = request.form['body']

        if not blog_title:
            flash("Please enter a blog title", "error_title")
        
        if not body:
            flash("Please enter text into the blog", "error_body")
        
        if blog_title and body:
            blog_post = Blog(blog_title, body)
            db.session.add(blog_post)
            db.session.commit()
            post = Blog.query.filter_by(body=body).first()

            return render_template('blogpage.html', post=post, blog_title=blog_title, body=body)

    return render_template('newpost.html', title="Add a Blog Entry", id=id, blog_title=blog_title, body=body)

@app.route('/')
def bloghome():
    return redirect('/blog')


@app.route('/blog', methods=['GET'])
def blog_listings():
    '''Display all blogs in the database, or just a specific post if an ID is passed in the GET'''
    posts = Blog.query.order_by(Blog.pub_date.desc()).all()

    if request.args.get('id'):
        post_id = request.args.get('id')
        post = Blog.query.filter_by(id=post_id).first()
        return render_template('blogpage.html', post=post)

    return render_template('blog.html', posts=posts, title="Build a Blog!")



if __name__ == '__main__':
    app.run()