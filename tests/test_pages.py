import unittest2 as unittest

import monitoring_app

class TestPages(unittest.TestCase):
    def setUp(self):
        self.app = monitoring_app.create_app()
        self.client = self.app.test_client()

    def test_index_page(self):
        """The index page should show the app's info and the correct route."""
        rv = self.client.get('/')
        assert self.app.config['APP_NAME'] in rv.data
        assert self.app.config['APP_DESCRIPTION'] in rv.data
        assert 'Home' in rv.data

    def test_examples_page(self):
        """The /examples route should resolve to /examples/table."""
        rv = self.client.get('/examples/table')
        rv_resolved = self.client.get('/examples')
        assert rv.data == rv_resolved.data

    def test_tabs_page(self):
        """The /examples/tabs route should resolve to /examples/tabs/tab1."""
        rv = self.client.get('/examples/tabs/tab1')
        rv_resolved = self.client.get('/examples/tabs')
        assert rv.data == rv_resolved.data


if __name__ == '__main__':
    unittest.main()
