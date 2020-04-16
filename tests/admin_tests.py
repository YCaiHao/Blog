from nose.tools import *
from flask import url_for

from app import db
from app.models import Post, Category

from tests.base import BaseTest

class TestAdmin(BaseTest):
    def setup(self):
        super().setup()
        self.login()

        category = Category(name='Unknown')
        post = Post(title='Hello', category=category, body='Blah...')
        db.session.add_all([category, post])
        db.session.commit()

    def test_new_post(self):
        response = self.client.get(url_for('admin.new_post'))
        data = response.get_data(as_text=True)
        assert_in('New Post', data)

        response = self.client.post(url_for('admin.new_post'), data=dict(
            title='Something',
            category=1,
            body='Hello, world.'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        assert_in('Post created.', data)
        assert_in('Something', data)
        assert_in('Hello, world.', data)

    def test_edit_post(self):
        response = self.client.get(url_for('admin.edit_post', post_id=1))
        data = response.get_data(as_text=True)
        assert_in('Edit Post', data)
        assert_in('Hello', data)
        assert_in('Blah...', data)

        response = self.client.post(url_for('admin.edit_post', post_id=1), data=dict(
            title='Something Edited',
            category=1,
            body='New post body.'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        assert_in('Post updated.', data)
        assert_in('New post body.', data)
        assert_not_in('Blah...', data)

    def test_delete_post(self):
        response = self.client.get(url_for('admin.delete_post', post_id=1), follow_redirects=True)
        data = response.get_data(as_text=True)
        assert_not_in('Post deleted.', data)
        assert_in('405 Method Not Allowed', data)

        response = self.client.post(url_for('admin.delete_post', post_id=1), follow_redirects=True)
        data = response.get_data(as_text=True)
        assert_in('Post deleted.', data)

    def test_new_category(self):
        response = self.client.post(url_for('admin.new_category'), data=dict(name='Tech'), follow_redirects=True)
        data = response.get_data(as_text=True)
        assert_in('Category created.', data)
        assert_in('Tech', data)

        response = self.client.post(url_for('admin.new_category'), data=dict(name='Tech'), follow_redirects=True)
        data = response.get_data(as_text=True)
        assert_in('Name already in use.', data)

        category = Category.query.get(1)
        post = Post(title='Post Title', category=category)
        db.session.add(post)
        db.session.commit()
        response = self.client.get(url_for('blog.show_category', category_id=1))
        data = response.get_data(as_text=True)
        assert_in('Post Title', data)
    
    def test_edit_category(self):
        response = self.client.post(url_for('admin.edit_category', category_id=1),
                                    data=dict(name='Unknown edited'), follow_redirects=True)
        data = response.get_data(as_text=True)
        assert_not_in('Category updated.', data)
        assert_in('Unknown', data)
        assert_not_in('Unknown edited', data)
        assert_in('You can not edit the Unknown category', data)

        response = self.client.post(url_for('admin.new_category'), data=dict(name='Tech'), follow_redirects=True)
        data = response.get_data(as_text=True)
        assert_in('Category created.', data)
        assert_in('Tech', data)

        response = self.client.get(url_for('admin.edit_category', category_id=2))
        data = response.get_data(as_text=True)
        assert_in('Edit Category', data)
        assert_in('Tech', data)

        response = self.client.post(url_for('admin.edit_category', category_id=2),
                                    data=dict(name='Life'), follow_redirects=True)
        data = response.get_data(as_text=True)
        assert_in('Category updated.', data)
        assert_in('Life', data)
        assert_not_in('Tech', data)

    def test_delete_category(self):
        category = Category(name='Tech')
        post = Post(title='test', category=category)
        db.session.add(category)
        db.session.add(post)
        db.session.commit()

        response = self.client.get(url_for('admin.delete_category', category_id=1), follow_redirects=True)
        data = response.get_data(as_text=True)
        assert_not_in('Category deleted.', data)
        assert_in('405 Method Not Allowed', data)

        response = self.client.post(url_for('admin.delete_category', category_id=1), follow_redirects=True)
        data = response.get_data(as_text=True)
        assert_in('You can not delete the Unknown category.', data)
        assert_not_in('Category deleted.', data)
        assert_in('Unknown', data)

        response = self.client.post(url_for('admin.delete_category', category_id=2), follow_redirects=True)
        data = response.get_data(as_text=True)
        assert_in('Category deleted.', data)
        assert_in('Unknown', data)
        assert_not_in('Tech', data)

    def test_manage_post_page(self):
        response = self.client.get(url_for('admin.manage_post'))
        data = response.get_data(as_text=True)
        assert_in('Manage Posts', data)

    def test_manage_category_page(self):
        response = self.client.get(url_for('admin.manage_category'))
        data = response.get_data(as_text=True)
        assert_in('Manage Categories', data)

    def test_blog_setting(self):
        response = self.client.post(url_for('admin.settings'), data=dict(
            name='Grey Li',
            blog_title='My Blog',
            bio='I am ...',
            about='Example about page',
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        assert_in('Setting updated.', data)
        assert_in('My Blog', data)

        response = self.client.get(url_for('admin.settings'))
        data = response.get_data(as_text=True)
        assert_in('Grey Li', data)
        assert_in('My Blog', data)

        response = self.client.get(url_for('blog.about'), follow_redirects=True)
        data = response.get_data(as_text=True)
        assert_in('Example about page', data)