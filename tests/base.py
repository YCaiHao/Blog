import click
from flask import url_for

from app import create_app, db
from app.models import Admin, Category, Post
from config import TestingConfig


class BaseTest(object):
    def setup(self):
        app = create_app(TestingConfig)
        @app.context_processor
        def make_template_context():
            admin = Admin.query.first()
            categories = Category.query.order_by(Category.name).all()
            return dict(
                admin=admin, categories=categories)
        @app.template_filter('md')
        def markdown_to_html(txt):
            from markdown import markdown
            return markdown(txt, extensions=[
                                    'markdown.extensions.extra',
                                    'markdown.extensions.codehilite'])
        @app.cli.command()
        @click.option('--drop', is_flag=True, help='Create after drop.')
        def initdb(drop):
            """Initialize the database."""
            if drop:
                click.confirm('This operation will delete the database, do you want to continue?', abort=True)
                db.drop_all()
                click.echo('Drop tables.')
            db.create_all()
            click.echo('Initialized database.')

        @app.cli.command()
        @click.option('--username', prompt=True, help='The username used to login.')
        @click.option('--password', prompt=True, hide_input=True,
                        confirmation_prompt=True, help='The password used to login.')
        def init(username, password):
            """Building Bluelog, just for you."""

            click.echo('Initializing the database...')
            db.create_all()

            admin = Admin.query.first()
            if admin is not None:
                click.echo('The administrator already exists, updating...')
                admin.username = username
                admin.set_password(password)
            else:
                click.echo('Creating the temporary administrator account...')
                admin = Admin(
                    username=username,
                    blog_title='Bluelog',
                    name='Admin',
                    about='Anything about you.'
                )
                admin.set_password(password)
                db.session.add(admin)

            category = Category.query.first()
            if category is None:
                click.echo('Creating the default category...')
                category = Category(name='Default')
                db.session.add(category)

            db.session.commit()
            click.echo('Done.')

        @app.cli.command()
        @click.option('--category', default=10, help='Quantity of categories, default is 10.')
        @click.option('--post', default=50, help='Quantity of posts, default is 50.')
        def forge(category, post):
            """Generate fake data."""
            from app.fakes import fake_admin, fake_categories, fake_posts

            db.drop_all()
            db.create_all()

            click.echo('Generating the administrator...')
            fake_admin()

            click.echo('Generating %d categories...' % category)
            fake_categories(category)

            click.echo('Generating %d posts...' % post)
            fake_posts(post)

            click.echo('Done.')

        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()

        db.create_all()
        user = Admin(name='YCH', username='grey', about='I am test', blog_title='Testlog')
        user.set_password('123')
        db.session.add(user)
        db.session.commit()

    def teardown(self):
        db.drop_all()
        self.context.pop()
    
    def login(self, username=None, password=None):
        if username is None and password is None:
            username = 'grey'
            password = '123'
        return self.client.post(url_for('auth.login'), data=dict(
            username=username,
            password=password,
        ), follow_redirects=True)

    def logout(self):
        return self.client.get(url_for('auth.logout'), follow_redirects=True)