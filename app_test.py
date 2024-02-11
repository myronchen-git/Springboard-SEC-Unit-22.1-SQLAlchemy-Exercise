from unittest import TestCase

from app import app
from models import User, db

# --------------------------------------------------

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test"
app.config["SQLALCHEMY_ECHO"] = False
db.drop_all()
db.create_all()

app.config["TESTING"] = True
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

# ==================================================


class FlaskTests(TestCase):
    """Tests for Blogly"""

    def setUp(self):
        """Remove existing users and add sample users."""

        User.query.delete()

        users = (
            User(
                first_name="George",
                last_name="Washington",
                image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Gilbert_Stuart_Williamstown_Portrait_of_George_Washington.jpg/330px-Gilbert_Stuart_Williamstown_Portrait_of_George_Washington.jpg",
            ),
            User(
                first_name="Abraham",
                last_name="Lincoln",
                image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg/330px-Abraham_Lincoln_O-77_matte_collodion_print.jpg",
            ),
        )
        db.session.add_all(users)
        db.session.commit()

        self.users = users

    def tearDown(self):
        """Clean up transactions."""

        db.session.rollback()

    def test_list_users(self):
        """Tests displaying the list of users."""

        with app.test_client() as c:
            # WHEN
            resp = c.get("/users")
            html = resp.get_data(as_text=True)

            # THEN
            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.users[0].full_name, html)
            self.assertIn(self.users[1].full_name, html)

    def test_add_user(self):
        """Tests adding a new user."""

        # GIVEN
        first_name = "Thomas"
        last_name = "Jefferson"
        image_url = ""

        with app.test_client() as c:
            # WHEN
            resp = c.post(
                "/users/new",
                data={
                    "first-name": first_name,
                    "last-name": last_name,
                    "image-url": image_url,
                },
                follow_redirects=True,
            )
            html = resp.get_data(as_text=True)
            user = User.query.filter_by(first_name=first_name).one()

            # THEN
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"{first_name} {last_name}", html)

            self.assertEqual(user.first_name, first_name)
            self.assertEqual(user.last_name, last_name)
            self.assertEqual(user.image_url, image_url)

    def test_edit_user(self):
        """Tests editing a user."""

        # GIVEN
        # Use George Washington
        new_first_name = "Ge"
        new_last_name = "Wa"
        new_image_url = ""
        user = User.query.filter_by(first_name=self.users[0].first_name).one()

        with app.test_client() as c:
            # WHEN
            resp = c.post(
                f"/users/{user.id}/edit",
                data={
                    "first-name": new_first_name,
                    "last-name": new_last_name,
                    "image-url": new_image_url,
                },
                follow_redirects=True,
            )
            html = resp.get_data(as_text=True)
            user = User.query.get(user.id)

            # THEN
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"{new_first_name} {new_last_name}", html)

            self.assertEqual(user.first_name, new_first_name)
            self.assertEqual(user.last_name, new_last_name)
            self.assertEqual(user.image_url, new_image_url)

    def test_delete_user(self):
        """Tests deleting a user."""

        # GIVEN
        # Use Abraham Lincoln
        user = User.query.filter_by(first_name=self.users[1].first_name).one()

        with app.test_client() as c:
            # WHEN
            resp = c.post(f"/users/{user.id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)
            user = User.query.filter_by(
                first_name=self.users[1].first_name
            ).one_or_none()

            # THEN
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(self.users[1].full_name, html)

            self.assertIsNone(user)
