""" Data Models """
from . import db


# Create Database for user
class User(db.Model):
    __tablename__ = "accounts"

    id = db.Column(
        db.Integer,
        primary_key=True

    )
    firstName = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    lastName = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False,
    )
    userName = db.Column(
        db.VARCHAR(64),
        index=False,
        unique=True,  # Unique means can't exist another user
        nullable=False,
    )
    email = db.Column(
        db.VARCHAR(64),
        nullable=False,
        unique=True,
        index=True,
    )
    password = db.Column(
        db.TEXT(100),
        unique=False,
        nullable=False,
    )

    def __repr__(self):
        return "<User {}".format(self.userName)

# class
