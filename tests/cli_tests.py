from nose.tools import *

from app import db
from app.models import Admin, Post, Category
from tests.base import BaseTest

class TestCLI(BaseTest):
    def setup(self):
        super().setup()
        db.drop_all()

    def test_initdb_command(self):
        result = self.runner.invoke(args=['initdb'])
        assert_in('Initialized database.', result.output)

    def test_initdb_command_with_drop(self):
        result = self.runner.invoke(args=['initdb', '--drop'], input='y\n')
        assert_in('This operation will delete the database, do you want to continue?', result.output)
        assert_in('Drop tables.', result.output)
    
    def test_init_command(self):
        result = self.runner.invoke(args=['init', '--username', 'grey', '--password', '123'])
        assert_in('Creating the temporary administrator account...', result.output)
        assert_in('Creating the default category...', result.output)
        assert_in('Done.', result.output)
        assert_equal(Admin.query.count(), 1)
        assert_equal(Admin.query.first().username, 'grey')
        assert_equal(Category.query.first().name, 'Default')

    def test_init_command_with_update(self):
        self.runner.invoke(args=['init', '--username', 'grey', '--password', '123'])
        result = self.runner.invoke(args=['init', '--username', 'new grey', '--password', '123'])
        assert_in('The administrator already exists, updating...', result.output)
        assert_not_in('Creating the temporary administrator account...', result.output)
        assert_equal(Admin.query.count(), 1)
        assert_equal(Admin.query.first().username, 'new grey')
        assert_equal(Category.query.first().name, 'Default')

    def test_forge_command(self):
        result = self.runner.invoke(args=['forge'])

        assert_equal(Admin.query.count(), 1)
        assert_in('Generating the administrator...', result.output)

        assert_equal(Post.query.count(), 50)
        assert_in('Generating 50 posts...', result.output)

        assert_equal(Category.query.count(), 10 + 1)
        assert_in('Generating 10 categories...', result.output)

        assert_in('Done.', result.output)

    def test_forge_command_with_count(self):
        result = self.runner.invoke(args=['forge', '--category', '5', '--post', '20'])
        assert_equal(Admin.query.count(), 1)
        assert_in('Generating the administrator...', result.output)

        assert_equal(Post.query.count(), 20)
        assert_in('Generating 20 posts...', result.output)

        assert_equal(Category.query.count(), 5 + 1)
        assert_in('Generating 5 categories...', result.output)

        assert_in('Done.', result.output)