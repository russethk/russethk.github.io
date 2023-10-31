""" Message model tests. """

# run these tests like:
# python -m unittest test_message_model.py

import os
from unittest import TestCase
from models import db, User, Message, Follows, Likes




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


class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        Likes.query.delete()

        self.client = app.test_client()

    def test_message_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        m = Message(
            text="test message",
            user_id=u.id
        )

        db.session.add(m)
        db.session.commit()

        # Message should have no likes
        self.assertEqual(len(m.likes), 0)

    def test_message_likes(self):
        """Does the likes relationship work?"""

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

        m = Message(
            text="test message",
            user_id=u1.id
        )

        db.session.add(m)
        db.session.commit()

        l = Likes(user_id=u2.id, message_id=m.id)
        db.session.add(l)
        db.session.commit()

        self.assertEqual(len(m.likes), 1)
        self.assertEqual(m.likes[0].user_id, u2.id)
        self.assertEqual(m.likes[0].message_id, m.id)

    def test_message_repr(self):
        """Does the repr method work as expected?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        m = Message(
            text="test message",
            user_id=u.id
        )

        db.session.add(m)
        db.session.commit()

        self.assertEqual(m.__repr__(), f"<Message #{m.id}: {m.text}, {m.timestamp}>")

    def test_message_delete(self):
        """Does the delete method work as expected?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        m = Message(
            text="test message",
            user_id=u.id
        )

        db.session.add(m)
        db.session.commit()

        db.session.delete(m)
        db.session.commit()

        self.assertEqual(len(Message.query.all()), 0)
        self.assertEqual(len(Likes.query.all()), 0)

    def test_message_delete_likes(self):
        """Does the delete method work as expected?"""

        u1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add_all([u1, u2])
        db.session.commit()

        m = Message(
            text="test message",
            user_id=u1.id
        )

        db.session.add(m)
        db.session.commit()

        l = Likes(user_id=u2.id, message_id=m.id)
        db.session.add(l)
        db.session.commit()

        db.session.delete(m)
        db.session.commit()

        self.assertEqual(len(Message.query.all()), 0)

    def test_message_delete_user(self):
        """Does the delete method work as expected?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        m = Message(
            text="test message",
            user_id=u.id
        )

        db.session.add(m)
        db.session.commit()

        db.session.delete(u)
        db.session.commit()

        self.assertEqual(len(Message.query.all()), 0)
        self.assertEqual(len(Likes.query.all()), 0)

    def test_message_delete_likes_user(self):
        """Does the delete method work as expected?"""

        u1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add_all([u1, u2])
        db.session.commit()

        m = Message(
            text="test message",
            user_id=u1.id
        )

        db.session.add(m)
        db.session.commit()

        l = Likes(user_id=u2.id, message_id=m.id)
        db.session.add(l)
        db.session.commit()

        db.session.delete(u1)
        db.session.commit()

        self.assertEqual(len(Message.query.all()), 0)

    def test_message_delete_likes_user2(self):
        """Does the delete method work as expected?"""

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

        m = Message(
            text="test message",
            user_id=u1.id
        )

        db.session.add(m)
        db.session.commit()

        l = Likes(user_id=u2.id, message_id=m.id)
        db.session.add(l)
        db.session.commit()

        db.session.delete(u2)
        db.session.commit()

        self.assertEqual(len(Message.query.all()), 1)

    def test_message_delete_likes_user3(self):
        """Does the delete method work as expected?"""

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

        u3 = User(
            email="test3@test.com",
            username="testuser3",
            password="HASHED_PASSWORD"
        )

        db.session.add_all([u1, u2, u3])
        db.session.commit()

        m = Message(
            text="test message",
            user_id=u1.id
        )

        db.session.add(m)
        db.session.commit()

        l1 = Likes(user_id=u2.id, message_id=m.id)
        l2 = Likes(user_id=u3.id, message_id=m.id)
        db.session.add_all([l1, l2])
        db.session.commit()

        db.session.delete(u2)
        db.session.commit()

        self.assertEqual(len(Message.query.all()), 1)
        self.assertEqual(len(Likes.query.all()), 1)
        self.assertEqual(Likes.query.first().user_id, u3.id)
