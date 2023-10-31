"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_repr(self):
        """Does the repr method work as expected?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(u.__repr__(), f"<User #{u.id}: {u.username}, {u.email}>")

    def test_is_following(self):
        """Does is_following successfully detect when user1 is following user2?"""

        u1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        db.session.add_all([u1, u2])
        db.session.commit()

        f = Follows(user_being_followed_id=u2.id, user_following_id=u1.id)
        db.session.add(f)
        db.session.commit()

        self.assertTrue(u1.is_following(u2))
        self.assertFalse(u2.is_following(u1))

    def test_is_followed_by(self):
        """Does is_followed_by successfully detect when user1 is followed by user2?"""

        u1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        db.session.add_all([u1, u2])
        db.session.commit()

        f = Follows(user_being_followed_id=u2.id, user_following_id=u1.id)
        db.session.add(f)
        db.session.commit()

        self.assertTrue(u2.is_followed_by(u1))
        self.assertFalse(u1.is_followed_by(u2))

    def test_signup(self):
        """Does User.signup successfully create a new user given valid credentials?"""

        u = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url=None
        )

        db.session.commit()

        self.assertEqual(u.email, "test@test.com")
        self.assertEqual(u.username, "testuser")
        self.assertNotEqual(u.password, "HASHED_PASSWORD")
        self.assertTrue(u.password.startswith("$2b$"))

    def test_signup_fail(self):
        """Does User.signup fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?"""

        u = User.signup(
            email="test#test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url=None
        )

        with self.assertRaises(Exception) as context:
            db.session.commit()

        self.assertTrue("invalid input syntax for type numeric: \"test#test.com\"" in str(context.exception))

    def test_authenticate(self):
        """Does User.authenticate successfully return a user when given a valid username and password?"""

        u = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url=None
        )

        db.session.commit()

        self.assertEqual(User.authenticate("testuser", "HASHED_PASSWORD"), u)

    def test_authenticate_fail(self):
        """Does User.authenticate fail to return a user when the username is invalid?"""

        u = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url=None
        )

        db.session.commit()

        self.assertFalse(User.authenticate("testuser2", "HASHED_PASSWORD"))

    def test_authenticate_fail(self):
        """Does User.authenticate fail to return a user when the password is invalid?"""

        u = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url=None
        )

        db.session.commit()

        self.assertFalse(User.authenticate("testuser", "HASHED_PASSWORD2"))

    def test_user_likes(self):
        """Does the user like a message?"""

        u = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url=None
        )

        m = Message(text="test message", user_id=u.id)

        db.session.add_all([u, m])
        db.session.commit()

        u.likes.append(m)
        db.session.commit()

        self.assertEqual(len(u.likes), 1)
        self.assertEqual(u.likes[0].text, "test message")

    def test_user_unlikes(self):
        """Does the user unlike a message?"""

        u = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url=None
        )

        m = Message(text="test message", user_id=u.id)

        db.session.add_all([u, m])
        db.session.commit()

        u.likes.append(m)
        db.session.commit()

        u.likes.remove(m)
        db.session.commit()

        self.assertEqual(len(u.likes), 0)

    def test_user_is_liking(self):
        """Is the user liking a message?"""

        u = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url=None
        )

        m = Message(text="test message", user_id=u.id)
        
        db.session.add_all([u, m])
        db.session.commit()

        u.likes.append(m)
        db.session.commit()

        self.assertTrue(u.is_liking(m))

    def test_user_is_not_liking(self):
        """Is the user not liking a message?"""

        u = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url=None
        )

        m = Message(text="test message", user_id=u.id)

        db.session.add_all([u, m])
        db.session.commit()

        self.assertFalse(u.is_liking(m))