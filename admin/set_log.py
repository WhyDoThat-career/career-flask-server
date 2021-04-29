import logging, json
from flask import has_request_context,request
from admin import app
from flask_login import current_user
from flask.logging import default_handler
from collections import OrderedDict
from jsonformatter import JsonFormatter
from kafka import KafkaProducer

class KafkaLoggingHandler(logging.Handler) :
    def __init__(self,hostlist,topic,tls=None) :
        logging.Handler.__init__(self)
        self.producer = KafkaProducer(acks=0, 
                         api_version=(2,3,0),
                         bootstrap_servers=hostlist,
                         value_serializer=lambda x: x.encode('utf-8')
                         )
        self.topic = topic
    def emit(self,record) :
        if 'kafka.' in record.name :
            return
        try :
            msg = self.format(record)
            json_msg = json.loads(msg)
            json_msg['Message'] = json.loads(json_msg['Message'].replace("\'","\""))
            json_msg = json.dumps(json_msg,ensure_ascii=False)
            self.producer.send(self.topic,json_msg)
            self.flush(timeout=1.0)
        except :
            logging.Handler.handleError(self, record)
    def flush(self, timeout=None) :
        self.producer.flush(timeout=timeout)
    def close(self) :
        self.acquire()
        try:
            if self.producer:
                self.producer.close()
            logging.Handler.close(self)
        finally:
            self.release()

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

kafka_handler = KafkaLoggingHandler(["52.78.62.228:9092"],topic='flask_all_logs')

default_handler.setFormatter(formatter)
kafka_handler.setFormatter(formatter)
app.logger.setLevel(logging.INFO)
app.logger.addHandler(kafka_handler)
app.logger.info(json.dumps({'info':'Flask server open'}))
