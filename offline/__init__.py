from flask import Blueprint
import webmonitor

from offline import job_resolvers

# Only export externally useful methods
__all__ = ['create_app', 'wsgi']


def create_app():
    app = webmonitor.create_app()
    app.config.from_object('offline.config')
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
    return create_app()(*args, **kwargs)


def add_logging(app):
    import logging
    file_handler = logging.FileHandler('log/offline.log')
    file_handler.setLevel(logging.DEBUG)
    # Send an email to the admins on ERROR
    mail_handler = logging.handlers.SMTPHandler(
        '127.0.0.1',
        'server-error@example.com', app.config.get('ADMINS'),
        'Monitoring app failed')
    mail_handler.setLevel(logging.ERROR)
    # Attach the handlers to the app
    app.logger.addHandler(file_handler)
    app.logger.addHandler(mail_handler)
