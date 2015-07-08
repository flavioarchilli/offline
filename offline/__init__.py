from flask import Blueprint,redirect
import webmonitor
import pprint

from offline import job_resolvers

# Only export externally useful methods
__all__ = ['create_app', 'wsgi']

def create_app():

    from offline.offline_blueprint import offline_bp
    from offline.histogramDB_tree_menu import histogramDB_tree_menu
    from offline.job_resolvers import tasks_resolver

    app = webmonitor.create_app()
    app.config.from_object('offline.config')
    
    if not app.debug:
        add_logging(app)
        app.logger.info('webmonitor startup')
    
    presenter = Blueprint('offline', __name__,
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='/{0}'.format(__name__))
    @presenter.route('/')
    def strange_fun():
       return redirect('/offline_bp') 

    @presenter.route('/ConfirmQuit')
    def logout_fun():
       return redirect('/offline_bp/ConfirmQuit')

    app.register_blueprint(presenter)
    app.register_blueprint(offline_bp, url_prefix='/offline_bp')

    app.register_blueprint(histogramDB_tree_menu, url_prefix='/histogramDB_tree_menu')

    app.add_job_resolver(tasks_resolver)

    return app


def wsgi(*args, **kwargs):
    return create_app()(*args, **kwargs)


def add_logging(app):
    import logging
    file_handler = logging.FileHandler('log/offline.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    # Send an email to the admins on ERROR
    mail_handler = logging.handlers.SMTPHandler(
        '127.0.0.1',
        'flavio.archilli@cern.ch', app.config.get('ADMINS'),
        'LHCb DQM failed')
    mail_handler.setLevel(logging.ERROR)
    # Attach the handlers to the app
    app.logger.addHandler(file_handler)
    app.logger.addHandler(mail_handler)

