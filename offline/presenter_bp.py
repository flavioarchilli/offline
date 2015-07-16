from flask import (
    Blueprint,
    current_app,
    request,
    flash,
    redirect,
    url_for,
    render_template,
    abort,
    jsonify,
    g
)

presenter = Blueprint('offline', __name__,
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='/{0}'.format(__name__))
@presenter.route('/')
def welcome_fun():
         page = render_template("Hello.html",
                                PROJECTBUTTONS = current_app.make_project_buttons())

         return page
   


