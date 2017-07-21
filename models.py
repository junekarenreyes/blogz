from app import db
import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def __repr__(self):
        return '<User %r>' % self.username

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(120))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)
    owner_id =  db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, blog_title, body, owner):
        self.blog_title = blog_title
        self.body = body
        self.pub_date = datetime.datetime.now()
        self.owner = owner
    
    def __repr__(self):
        return '<Blog %r>' % self.blog_title

