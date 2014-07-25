from flask import Blueprint
import webmonitor

from monitoring_app import job_resolvers

# Only export externally useful methods
__all__ = ['create_app', 'wsgi']


def create_app():
    """Create a Flask application deriving from webmonitor."""
    app = webmonitor.create_app()
    app.config.from_object('monitoring_app.config')

    if not app.debug:
        add_logging(app)

    example = Blueprint('example', __name__,
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='/{0}'.format(__name__))
    app.register_blueprint(example)

    app.add_job_resolver(job_resolvers.tasks_resolver)

    return app


def wsgi(*args, **kwargs):
    """Create an app and pass it arguments from a WSGI server, like gunicorn.

    With this, run with something like `gunicorn monitoring_app:wsgi`.
    """
    return create_app()(*args, **kwargs)


def add_logging(app):
    """Add log-to-file and log-to-mail to a Flask app."""
    import logging
    # Record to file on WARNING
    file_handler = logging.FileHandler('log/monitoring_app.log')
    file_handler.setLevel(logging.WARNING)
    # Send an email to the admins on ERROR
    mail_handler = logging.handlers.SMTPHandler(
        '127.0.0.1',
        'server-error@example.com', app.config.get('ADMINS'),
        'Monitoring app failed')
    mail_handler.setLevel(logging.ERROR)
    # Attach the handlers to the app
    app.logger.addHandler(file_handler)
    app.logger.addHandler(mail_handler)
