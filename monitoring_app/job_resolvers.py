def tasks_resolver(name):
    """Append tasks module path to name if it is an allowed task."""
    if name in ('list_file', 'get_key_from_file'):
        return 'monitoring_app.tasks.{0}'.format(name)
    return None
