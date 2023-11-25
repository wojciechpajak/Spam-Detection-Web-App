from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    rates = db.relationship('RateHistory', backref='user', lazy=True)

    def __repr__(self):
        return f"id: {self.id}, username:{self.username}, email:{self.email}"


class RateHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    model = db.Column(db.String, nullable=False)
    rate = db.Column(db.Float, nullable=False)
    ham_rate = db.Column(db.Float, nullable=False)
    spam_rate = db.Column(db.Float, nullable=False)
    plot = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"id: {self.id}, content:{self.content}, model:{self.model}, rate:{self.rate}"


class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    accuracy = db.Column(db.Float)
    precision = db.Column(db.Float)
    recall = db.Column(db.Float)
    f1_score = db.Column(db.Float)
    std_deviation = db.Column(db.Float)

    def __repr__(self):
        return f"model:{self.name}, accuracy:{self.accuracy}, precision:{self.precision}, recall: {self.recall}, f1_score:{self.f1_score}, std_deviation: {self.std_deviation}"
