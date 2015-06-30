def tasks_resolver(name):
    """Append tasks module path to name if it is an allowed task."""
    if name in ('list_file', 'get_key_from_file'):
        return 'presemter.tasks.{0}'.format(name)
    return None

def offline_resolver(name):
    """Append module path to name if it is an allowed task."""
    if name in ('list_file', 'get_key_from_file'):
        return 'presemter.offline_tasks.{0}'.format(name)
    return None


