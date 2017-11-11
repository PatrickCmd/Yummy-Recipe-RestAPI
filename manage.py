# manage.py
# configurations for running migrations


import os
import unittest
import coverage

from flask_script import Manager  # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand

Cov = coverage.coverage(
    branch=True,
    include='api/*',
    omit=[
        'test/*',
        'api/config.py',
        'api/*/__init__.py'
    ]
)
Cov.start()

from api.config import app_config
from api import app, db, models

config_name = os.environ['APP_SETTINGS']
app.config.from_object(app_config[config_name])
migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the tests without test coverage"""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def test_cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful:
        Cov.stop()
        Cov.save()
        print('Coverage summary')
        Cov.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.joi(basedir, 'tmp/coverage')
        Cov.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        Cov.erase()
        return 0
    return 1


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables"""
    db.drop_all()


if __name__ == '__main__':
    manager.run()
