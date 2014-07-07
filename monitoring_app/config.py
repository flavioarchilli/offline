# Application name, used in page titles etc.
APP_NAME = 'Example app'

# Description, shown in the <meta> tag
APP_DESCRIPTION = 'An example app based on the WebMonitor.'

# List of emails to send ERROR messages to
ADMINS = ['admin@example.com']

# Mappings of parent paths to their default children
# The key represents the visited path, the value is the page that's served
# For the dict below, a visited path of `examples` will show the
# `examples/table` page, as an example
DEFAULT_CHILDREN = {
    '': 'home',
    'examples': 'examples/table',
    'examples/tabs': 'examples/tabs/tab1'
}
