from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Initialize db object — but DO NOT call db.init_app() here
db = SQLAlchemy()
wishlist_table = db.Table('wishlist',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    wishlist = db.relationship('Product', secondary=wishlist_table, backref='wishlisted_by')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(100))

