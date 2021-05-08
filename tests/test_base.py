import unittest
from flask import Flask
from flask_mux import Mux


class FlaskMuxBaseTest(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.mux = Mux(self.app)
        self.client = self.app.test_client()
