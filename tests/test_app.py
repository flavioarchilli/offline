import unittest2 as unittest

import monitoring_app

class TestPages(unittest.TestCase):
    def setUp(self):
        self.app = monitoring_app.create_app()
        self.client = self.app.test_client()

    def test_app_should_instantiate_with_tasks_resolver(self):
        """App should instantiate with the correct job resolvers."""
        assert len(self.app.job_resolvers()) == 1
        assert self.app.job_resolvers()[0] == monitoring_app.job_resolvers.tasks_resolver
