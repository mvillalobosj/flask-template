import json
import logging
import logging.config
from time import time

from apispec import APISpec
from flask import (
    current_app, g, Flask, jsonify, redirect, request, session, url_for)
from flask_apispec.extension import FlaskApiSpec
from flask.json import JSONEncoder
from werkzeug.exceptions import default_exceptions

from app.blueprints.user import user_blueprint
from app.utilities.db import get_db
from app.utilities.config import get_config
from app.utilities.http import APIError, make_json_error, RedirectException, SC


config = get_config()
logging.config.dictConfig(config.logging_config)


def setup_error_handlers(app):
    # make all error responses json
    for code in default_exceptions.keys():
        app.register_error_handler(code, make_json_error)

    @app.errorhandler(APIError)
    def handle_api_error(e):
        response = jsonify(e.serialize)
        response.status_code = e.status_code
        return response

    @app.errorhandler(RedirectException)
    def handle_redirect_error(e):
        return redirect(url_for(e.endpoint), code=e.code)

    @app.errorhandler(SC.UNPROCESSABLE)
    def handle_flask_apispec_errors(err):
        exc = getattr(err, 'exc')
        messages = exc.messages if exc else ['Invalid request']
        return jsonify({'messages': messages}), SC.UNPROCESSABLE

    # Catch 500's
    @app.errorhandler(SC.SERVERERR)
    def handle_exceptions(error):
        if config.app.debug:
            raise
        return make_json_error(error)


def setup_base_routes(app):
    @app.route('/heartbeat')
    def heartbeat():
        """A Simple Healthcheck to determine whether or not the app is up"""
        return "OK", SC.OK

    @app.route('/hello')
    def hello():
        return "Hello World", SC.OK


def setup_event_hooks(app):
    @app.before_request
    def before_request():
        g.db = get_db()
        g.request_time = time()
        session["user_id"] = "1"
        session["role"] = "admin"

    @app.after_request
    def after_request(response):
        g.response_status_code = response.status_code
        return response

    @app.teardown_request
    def teardown_request(exception=None):

        if hasattr(current_app, 'db'):
            current_app.db.close()
            current_app.db.remove()

        # Log how long this request took to complete.
        delta = 0
        if hasattr(g, 'request_time'):
            delta = (time() - g.request_time) * 1000  # report in milliseconds

        if hasattr(g, 'response_status_code') and g.response_status_code:
            response_status_code = g.response_status_code
        else:
            # g has no `response_status_code` attr if it's a 500
            response_status_code = 500

        url_params = request.url.split('?')
        if len(url_params) > 1:
            params = url_params[1]
        else:
            params = None

        if request.url_rule:
            rule = request.url_rule.rule
            endpoint = request.url_rule.endpoint
        else:
            rule = None
            endpoint = None

        try:
            body = json.loads(request.data.decode("utf-8"))
        except ValueError:
            body = None

        app.logger.info({
            'msg': 'App API Request',
            'url': request.base_url,
            'method': request.method,
            'params': params,
            'view_args': request.view_args,
            'body': body,
            'rule': rule,
            'endpoint': endpoint,
            'status_code': response_status_code,
            'milliseconds': delta,
            'user_id': session.get("user_id") or 'user_logged_out',
            'requestor_ip': request.remote_addr
        })

    @app.context_processor
    def utility_processor():
        return dict(
            ts=time
        )


def setup_swagger(app):
    app.config.update({
        'APISPEC_SPEC': APISpec(
            title='Flask Template',
            version='v1',
            plugins=['apispec.ext.marshmallow'],
            securityDefinitions={
                "json-web-token": {
                    "in": "header",
                    "name": "Authorization",
                    "type": "apiKey"
                }
            },
            tags=[]
        ),
        'APISPEC_SWAGGER_URL': '/swagger.json'
    })
    docs = FlaskApiSpec(app)
    docs.register_existing_resources()


def configure_app(app):
    app.config["SECRET_KEY"] = config.db.postgres.secret_key
    app.json_encoder = JSONEncoder


def setup_blueprints(app):
    app.register_blueprint(user_blueprint, url_prefix='/user')


def create_app():
    app = Flask(__name__)

    configure_app(app)
    setup_error_handlers(app)
    setup_base_routes(app)
    setup_event_hooks(app)
    setup_blueprints(app)
    setup_swagger(app)

    app.logger.info('App Initialized')

    return app
