import unittest2 as unittest

import monitoring_app

class TestPages(unittest.TestCase):
    def setUp(self):
        self.resolver = monitoring_app.job_resolvers.tasks_resolver

    def test_resolver_should_resolve_tasks(self):
        """Resolver should resolve the two allowed tasks."""
        for task in ('list_file', 'get_key_from_file'):
            assert self.resolver(task) is not None

    def test_resolver_should_not_resolve_invalid_tasks(self):
        """Resovler should return None for disallowed or invalid tasks."""
        # An actual Python builtin
        assert self.resolver('str') is None
        # A fake task name
        assert self.resolver('foobar') is None
        # Shouldn't allow the full from the client, either
        assert self.resolver('monitoring_app.tasks.list_file') is None
