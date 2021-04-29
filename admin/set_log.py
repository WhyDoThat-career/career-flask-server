import logging
from flask import has_request_context,request
from admin import app
from flask_login import current_user
from flask.logging import default_handler
from collections import OrderedDict
from jsonformatter import JsonFormatter

RECORD_CUSTOM_ATTRS = {
    # no parameters
    'url': lambda: request.url if has_request_context() else None,
    'user': lambda: current_user.id.hex if has_request_context() and current_user.is_active else None,
    'email' : lambda: current_user.email if has_request_context() and current_user.is_active else None,
    # Arbitrary keywords parameters
    'status': lambda **record_attrs: 'failed' if record_attrs['levelname'] in ['ERROR', 'CRITICAL'] else 'success'
}

RECORD_CUSTOM_FORMAT = OrderedDict([
    # custom record attributes start
    ("Url", "url"),
    ("User", "user"),
    ("Email", "email"),
    ("Status", "status"),
    # custom record attributes end
    ("Name", "name"),
    ("Levelno", "levelno"),
    ("Levelname", "levelname"),
    ("Pathname", "pathname"),
    ("Module", "module"),
    ("Lineno", "lineno"),
    ("FuncName", "funcName"),
    ("Asctime", "asctime"),
    ("Message", "message")
])

formatter = JsonFormatter(
    RECORD_CUSTOM_FORMAT,
    record_custom_attrs=RECORD_CUSTOM_ATTRS,
    ensure_ascii=False
)
default_handler.setFormatter(formatter)
app.logger.setLevel(logging.INFO)
# gunicorn_error_handlers = logging.getLogger('gunicorn.error').handlers
# app.logger.handlers.extend(gunicorn_error_handlers)
app.logger.info('my info')
app.logger.debug('debug message')
app.logger.warning('warning message')
app.logger.info('my info')
app.logger.info('my info')
app.logger.warning('warning message')
app.logger.warning('warning message')