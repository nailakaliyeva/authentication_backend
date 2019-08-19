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

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "orders": self.orders,
            "name": self.name,
            "isAdmin": self.isAdmin,
            "country": self.country,
            "state": self.state,
            "city": self.city,
            "address": self.address,
            "zipcode": self.zipcode,
            "password_hash": self.password_hash
        }


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase_date = db.Column(db.Integer, nullable=False)
    confirmation_number = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    products = db.relationship('Products', backref='orders', lazy=True)

    def __repr__(self):
        return '<Orders %r>' % self.purchase_date

    def serialize(self):
        return {
            "id": self.id,
            "purchase_date": self.purchase_date,
            "confirmation_number": self.confirmation_number,
            "user_id": self.user_id,
            "products": self.products
        }

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plan_name = db.Column(db.String(30), unique=True, nullable=True)
    price = db.Column(db.Integer, unique=True, nullable=False)
    orders_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    mag_f = db.relationship('Magfield', backref='product', lazy=True)
    temp = db.relationship('Tempfield', backref='product', lazy=True)
    atmo_pressure = db.relationship('Atmopressure', backref='product', lazy=True)
    axis_measure = db.relationship('Axismeasure', backref='product', lazy=True)

    def __repr__(self):
        return '<Products %r>' % self.plan_name

    def serialize(self):
        return {
            "id": self.id,
            "plan_name": self.plan_name,
            "price": self.price,
            "orders_id": self.orders_id,
            "mag_f": self.mag_f,
            "temp": self.temp,
            "atmo_pressure": self.atmo_pressure,
            "axis_measure": self.axis_measure
        }



class Magfield(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x_measure = db.Column(db.String(30), unique=True, nullable=False)
    y_measure = db.Column(db.String(30), unique=True, nullable=False)
    z_measure = db.Column(db.String(30), unique=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return '<Magfield %r>' % self.x_measure

    def serialize(self):
        return {
            "id": self.id,
            "x_measure": self.x_measure,
            "y_measure": self.y_measure,
            "z_measure": self.z_measure
        }


class Tempfield(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tempF = db.Column(db.Integer, unique=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return '<Tempfield %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "tempF": self.tempF
        }


class Atmopressure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    millibars = db.Column(db.Integer, unique=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return '<Atmopressure %r>' % self.millibars

    def serialize(self):
        return {
            "id": self.id,
            "millibars": self.millibars
        }

class Axismeasure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pitch = db.Column(db.Integer, unique=True, nullable=False)
    roll = db.Column(db.Integer, unique=True, nullable=False)
    yaw = db.Column(db.Integer, unique=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return '<Axismeasure %r>' % self.pitch

    def serialize(self):
        return {
            "id": self.id,
            "pitch": self.pitch,
            "roll": self.roll
        }
