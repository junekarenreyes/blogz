from flask import request, redirect, render_template, session, flash
# from flask_sqlalchemy import SQLAlchemy
# from models import User, Movie
import cgi
import pytz
from app import app, db
from models import User,Blog

#You're able to submit a new post at the /newpost route. 
#After submitting a new post, your app displays the main blog page.
@app.route("/newpost", methods=['POST', 'GET'])
def postblog():
    blog_title = ""
    body = ""
    user = User.query.filter_by(username=session['user']).first()
    
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        body = request.form['body']

        if not blog_title:
            flash("Please enter a blog title", "error_title")
        
        if not body:
            flash("Please enter text into the blog", "error_body")
        
        if blog_title and body:
            blog_post = Blog(blog_title, body, user)
            db.session.add(blog_post)
            db.session.commit()
            post = Blog.query.filter_by(body=body).first()

            return render_template('blogpage.html', post=post, blog_title=blog_title, body=body, user=user)

    return render_template('newpost.html', title="Add a Blog Entry", id=id, blog_title=blog_title, body=body, user=user)

'''
@app.route('/blog', methods=['GET'])
def blog_listings():
    owner = User.query.filter_by(email=session['user']).first()
    posts = Blog.query.filter_by(owner=owner).all()

    if request.args.get('id'):
        post_id = request.args.get('id')
        post = Blog.query.filter_by(id=post_id).first()
        return render_template('singleUser.html', post=post)

    return render_template('singleUser.html', posts=posts, title="Build a Blog!")
'''


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = User.query.filter_by(username=username)
        if username == "":
            flash('please enter a username and password')
        elif users.count() == 1:
            user = users.first()
            if password == user.password:
                session['user'] = user.username
                return redirect("/newpost")
            else:
                flash('password is incorrect')
        elif users.count() == 0:
                flash('username does not exist')
        return render_template('login.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        username_db_count = User.query.filter_by(username=username).count()
        if username == "":
            flash('please enter a username')
        elif password == "":
            flash('please enter a password')
        elif len(password) < 4:
            flash('password should be longer than 3 characters, please try again')
        elif username_db_count > 0:
            flash('yikes! "' + username + '" is already taken')
        elif password != verify:
            flash('passwords did not match')
        else:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            session['user'] = user.username
            return redirect("/newpost")
        return render_template('signup.html', username=username)

    if request.method == 'GET':
        return render_template('signup.html')

'''def is_email(string):
    # for our purposes, an email string has an '@' followed by a '.'
    # there is an embedded language called 'regular expression' that would crunch this implementation down
    # to a one-liner, but we'll keep it simple:
    atsign_index = string.find('@')
    atsign_present = atsign_index >= 0
    if not atsign_present:
        return False
    else:
        domain_dot_index = string.find('.', atsign_index)
        domain_dot_present = domain_dot_index >= 0
        return domain_dot_present'''



@app.route("/logout", methods=['GET'])
def logout():
    del session['user']
    return redirect("/blogz")


@app.route('/blogz', methods=['GET'])
def blog_listings():
    posts = Blog.query.order_by(Blog.pub_date.desc()).all()

    if request.args.get('username'):
        post_user = request.args.get('username')
        username = User.query.filter_by(username=post_user).first()
        posts = Blog.query.filter_by(owner=username).all()
        return render_template('singleUser.html', posts=posts, title="blogz posts!", post_user=post_user, username=username)

    if request.args.get('id'):
        post_id = request.args.get('id')
        post = Blog.query.filter_by(id=post_id).first()
        '''post contains the first blog post, owner id and id connect it to User'''
        user = User.query.filter_by(id=post.owner_id).first()
        return render_template('blogpage.html', post=post, user=user)
    
    return render_template('blog.html', posts=posts, title="All the Blogz Postz")


@app.route("/")
def index():
    users = User.query.filter_by().all()
    return render_template('index.html', users=users, title="Blogz Userz!")

def logged_in_user():
    owner = User.query.filter_by(username=session['user']).first()
    return owner

endpoints_without_login = ['blog_listings', 'signup', 'login', 'index']

@app.before_request
def require_login():
    if not ('user' in session or request.endpoint in endpoints_without_login):
        return redirect("/signup")

# In a real application, this should be kept secret (i.e. not on github)
# As a consequence of this secret being public, I think connection snoopers or
# rival movie sites' javascript could hijack our session and act as us,
# perhaps giving movies bad ratings - the HORROR.
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RU'


if __name__ == '__main__':
    app.run()