import unittest

from flask import current_app
from flask_testing import TestCase

from api import app
from api.config import app_config


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        config_name = 'development'
        app.config.from_object(app_config[config_name])
        return app

    def test_app_is_development(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'secret_key')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == \
            'postgresql://postgres:arsenal2016@localhost/yummy_api'
        )


class TestTestingConfig(TestCase):
    def create_app(self):
        config_name = 'testing'
        app.config.from_object(app_config[config_name])
        return app

    def test_app_is_testing(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'secret_key')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == \
            'postgresql://postgres:arsenal2016@localhost/yummy_api_test'
        )


class TestProductionConfig(TestCase):
    def create_app(self):
        config_name = 'production'
        app.config.from_object(app_config[config_name])
        return app

    def test_app_is_development(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'secret_key')
        self.assertTrue(app.config['DEBUG'] is False)


if __name__ == '__main__':
    unittest.main()