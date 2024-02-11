"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User for Blogly."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text)

    def __repr__(self):
        """Show info about user."""

        return (
            f"<User("
            f"id={self.id}, "
            f"first_name={self.first_name}, "
            f"last_name={self.last_name}, "
            f"image_url={self.image_url})>"
        )

    @property
    def full_name(self):
        """Property for returning the full name."""

        return f"{self.first_name} {self.last_name}"
