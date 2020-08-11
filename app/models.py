"""Database models."""
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """Model for user accounts."""

    __tablename__ = 'session-users'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(200),
        nullable=False,
        unique=False
    )
    email = db.Column(
        db.String(40),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False
    )
    website = db.Column(
        db.String(60),
        index=False,
        unique=False,
        nullable=True
    )
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    last_login = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.name)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()


class Post(db.Model):
    """Model for users' posts."""

    __tablename__ = 'posts'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('session-users.id', ondelete='CASCADE'),
        nullable=False
    )
    text = db.Column(
        db.Text
    )
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    @staticmethod
    def get_posts(n):
        return Post.query.select_from().order_by(Post.created_on.desc()).limit(n)
