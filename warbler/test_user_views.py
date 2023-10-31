""" User View tests. """

import os
from unittest import TestCase

from models import db, User, Message, Follows, Likes

# run these tests like:
# python -m unittest test_user_views.py


# before we import our app, we need to set an environmental variable
# to use a different database for tests (since we don't want to overwrite
# our development database)

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (once for all tests) and add sample data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        Likes.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)
        
        self.testuser2 = User.signup(username="testuser2",
                                    email="test2@test.com",
                                    password="testuser2",
                                    image_url=None)
        
        db.session.commit()

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_users_index(self):
        """Test users index page."""

        with self.client as c:
            resp = c.get("/users")

            self.assertIn("@testuser", str(resp.data))
            self.assertIn("@testuser2", str(resp.data))

    def test_users_search(self):
        """Test users search page."""

        with self.client as c:
            resp = c.get("/users?q=test")

            self.assertIn("@testuser", str(resp.data))
            self.assertIn("@testuser2", str(resp.data))

    def test_user_show(self):
        """Test user show page."""

        with self.client as c:
            resp = c.get(f"/users/{self.testuser.id}")

            self.assertEqual(resp.status_code, 200)
            self.assertIn("@testuser", str(resp.data))

    def test_user_following(self):
        """Test user following page."""

        with self.client as c:
            resp = c.get(f"/users/{self.testuser.id}/following")

            self.assertEqual(resp.status_code, 200)
            self.assertIn("@testuser", str(resp.data))

    def test_user_followers(self):
        """Test user followers page."""

        with self.client as c:
            resp = c.get(f"/users/{self.testuser.id}/followers")

            self.assertEqual(resp.status_code, 200)
            self.assertIn("@testuser", str(resp.data))  

    def test_user_follow(self):
        """Test user follow functionality."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            resp = c.post(f"/users/follow/{self.testuser2.id}", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("@testuser2", str(resp.data))
            self.assertIn("@testuser", str(resp.data))

    def test_user_unfollow(self):
        """Test user unfollow functionality."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            resp = c.post(f"/users/follow/{self.testuser2.id}", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("@testuser2", str(resp.data))
            self.assertIn("@testuser", str(resp.data))

            resp = c.post(f"/users/stop-following/{self.testuser2.id}", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("@testuser2", str(resp.data))
            self.assertIn("@testuser", str(resp.data))

    def test_user_profile(self):
        """Test user profile page."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            resp = c.get(f"/users/profile")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("@testuser", str(resp.data))

    def test_user_profile_edit(self):
        """Test user profile edit page."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            resp = c.get(f"/users/profile/edit")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("@testuser", str(resp.data))

    def test_user_profile_delete(self):
        """Test user profile delete page."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            resp = c.get(f"/users/delete")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("@testuser", str(resp.data))

    def test_user_profile_delete_confirm(self):
        """Test user profile delete confirm page."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            resp = c.post(f"/users/delete", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("@testuser", str(resp.data))

    def test_user_profile_delete_confirm_fail(self):
        """Test user profile delete confirm page."""

        with self.client as c:
            resp = c.post(f"/users/delete", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("@testuser", str(resp.data))

    def test_user_profile_edit_confirm(self):
        """Test user profile edit confirm page."""

        with self.client as c:
            resp = c.post(f"/users/profile/edit", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("@testuser", str(resp.data))

    def test_user_profile_edit_confirm_fail(self):
        """Test user profile edit confirm page."""

        with self.client as c:
            resp = c.post(f"/users/profile/edit", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("@testuser", str(resp.data))

