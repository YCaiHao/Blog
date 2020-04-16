from nose.tools import *
from flask import url_for

from app import db
from app.models import Post, Category

from tests.base import BaseTest

class TestBlog(BaseTest):
    def setup(self):
        super().setup()
        self.login()

        category = Category(name='Default')
        post = Post(title='Hello Post', category=category, body='Blah...')

        db.session.add_all([category, post])
        db.session.commit()

    def test_index_page(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        assert_in('Home', data)
        assert_in('Testlog', data)

    def test_post_page(self):
        response = self.client.get(url_for('blog.show_post', post_id=1))
        data = response.get_data(as_text=True)
        assert_in('Hello Post', data)

    def test_about_page(self):
        response = self.client.get(url_for('blog.about'))
        data = response.get_data(as_text=True)
        assert_in('I am test', data)
        assert_in('About', data)

    def test_category_page(self):
        response = self.client.get(url_for('blog.show_category', category_id=1))
        data = response.get_data(as_text=True)
        assert_in('Category: Default', data)
        assert_in('Hello Post', data)
