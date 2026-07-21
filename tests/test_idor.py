import sqlite3
import unittest
from pathlib import Path

import app as demo_app


class IdorBehaviorTests(unittest.TestCase):
    def setUp(self):
        demo_app.init_db()
        conn = sqlite3.connect(demo_app.DB_PATH)
        cur = conn.cursor()
        cur.execute("UPDATE profiles SET notes = ? WHERE id = 1", ("Profile note",))
        cur.execute("UPDATE profiles SET notes = ? WHERE id = 2", ("Profile note",))
        conn.commit()
        conn.close()
        self.client = demo_app.app.test_client()

    def test_default_view_shows_current_user_profile_without_flag(self):
        self.client.post(
            "/login",
            data={"username": "alice", "password": "password123"},
            follow_redirects=True,
        )

        response = self.client.get("/idor")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Current user: alice", response.data)
        self.assertIn(b"Profile note", response.data)
        self.assertNotIn(b"idor_missing_authorization", response.data)

    def test_other_user_profile_includes_flag_when_viewing_unauthorized_profile(self):
        self.client.post(
            "/login",
            data={"username": "alice", "password": "password123"},
            follow_redirects=True,
        )

        response = self.client.get("/idor?id=2")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Bob Example", response.data)
        self.assertIn(b"idor_missing_authorization", response.data)


if __name__ == "__main__":
    unittest.main()
