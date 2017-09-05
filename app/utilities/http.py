from flask import jsonify
from werkzeug.exceptions import HTTPException


class SC:
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    UNPROCESSABLE = 422
    SERVERERR = 500
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    TIMEOUT = 504


def make_json_error(ex, **kwargs):
    response = jsonify(message=str(ex), **kwargs)
    response.status_code = (
        ex.code if isinstance(ex, HTTPException) else SC.SERVERERR)
    return response


class APIError(Exception):
    """
    See http://flask.pocoo.org/docs/0.10/patterns/apierrors/ for reference.
    """

    STATUS_CODE = SC.BAD_REQUEST

    def __init__(self, message, status_code=None, error=None, env=None):
        Exception.__init__(self)
        self.message = message
        if env in ["dev", "dev-local"]:
            self.message = str(error)
        if status_code is not None:
            self.status_code = status_code

    @property
    def serialize(self):
        return dict(
            message=self.message
        )


class RedirectException(Exception):
    """
    Registered as a Flask errorhandler; raise to trigger a redirect
    """

    def __init__(self, endpoint, code=None):
        """ Initializing this class with an endpoint and status code
        will trigger a redirect accordingly.

        Args:
            endpoint (str) - The name of the Flask endpoint to redirect
                to
            code (int) - The HTTP status code to redirect with
        """
        self.endpoint = endpoint
        self.code = code
