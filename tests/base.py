from flask_testing import TestCase

from api.config import app_config
from api import app, db


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        config_name = 'testing'
        app.config.from_object(app_config[config_name])
        return app

    def setUp(self):
        # binds the app to the current context
        app = self.create_app()
        with app.app_context():
            # create all database tables
            db.create_all()
            db.session.commit()

    def tearDown(self):
        app = self.create_app()
        with app.app_context():
            # create all database tables
            db.session.remove()
            db.drop_all()