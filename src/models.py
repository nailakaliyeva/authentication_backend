from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Person %r>' % self.username

    def serialize(self):
        return {
            "username": self.username,
            "email": self.email
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orders = db.relationship('Orders', backref='user', lazy=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), unique=False, nullable=False)
    isAdmin = db.Column(db.Boolean, default=False)
    country = db.Column(db.String(30), unique=False, nullable=False)
    state = db.Column(db.String(30), unique=False, nullable=False)
    city = db.Column(db.String(30), unique=False, nullable=False)
    address = db.Column(db.String(30), unique=False, nullable=False)
    zipcode = db.Column(db.String(30), unique=False, nullable=False)
    password_hash = db.Column(db.String(120))


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase_date = db.Column(db.Integer(120), nullable=False)
    confirmation_number = db.Column(db.Integer(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product = db.relationship('Products', backref='product', lazy=True)

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plan_name = db.Column(db.String(30), unique=True, nullable=True)
    price = db.Column(db.Integer(30), unique=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)




