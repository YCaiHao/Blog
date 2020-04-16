from nose.tools import *

from flask import url_for

from tests.base import BaseTest

class TestAuth(BaseTest):
    def test_login_user(self):
        response = self.login()
        data = response.get_data(as_text=True)
        assert_in('Welcome back.', data)

    def test_fail_login(self):
        response = self.login(username='wrong-username', password='wrong-password')
        data = response.get_data(as_text=True)
        assert_in('Invalid username or password.', data)

    def test_logout_user(self):
        self.login()
        response = self.logout()
        data = response.get_data(as_text=True)
        assert_in('Logout success.', data)
    
    def test_login_protect(self):
        response = self.client.get(url_for('admin.settings'), follow_redirects=True)
        data = response.get_data(as_text=True)
        assert_in('Please log in to access this page.', data)