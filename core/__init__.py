from flask import Flask, url_for, request ,redirect
# from flask_socketio import SocketIO, emit
from flask_caching import Cache
import os, time
import datetime
from datetime import datetime as dt
import traceback
import logging
# import flask_profiler
app = Flask(__name__,static_url_path='/static')


app.config.from_object('core.config.SECRET_KEY')
app.config.from_object('core.config.ProductionConfig')

app.config["DEBUG"] = True

app.config['SESSION_COOKIE_DOMAIN'] = '.urbanedge.co.in'

# app.config["flask_profiler"] = {
#     "enabled": app.config["DEBUG"],
#     "storage": {
#         "engine": "sqlite"
#     },
#     "basicAuth":{
#         "enabled": True,
#         "username": "admin",
#         "password": "admin"
#     },
#     "ignore": [
#         "^/static/.*"
#     ]
# }




# print(datetime.datetime.now())

# the below 2 lines comment by ganesan
os.environ['TZ'] ='Asia/Calcutta'
time.tzset()


# print(datetime.datetime.now())

config = app.config
from core.library.cryptography import Cryptography
from core.library.helper import Helper
from core.model.Log import Log

cache = Cache(app,config={'CACHE_TYPE': 'FileSystemCache','CACHE_DIR':'file_cache'})
current_app = app

# socketio = SocketIO(app)

# from core import routes
# from core.controller.UserController import app as user
from core.controller.SessionsController import app as sessions
from core.controller.SessionChatController import app as s_chart
from core.controller.PosterController import app as poster
from core.controller.CertificateController import app as certify

from core.controller.BOController import app as backoffice

from core.controller.CommentsController import app as comments



# app.register_blueprint(user, url_prefix='')
app.register_blueprint(sessions, url_prefix='')
app.register_blueprint(s_chart, url_prefix='')
app.register_blueprint(poster, url_prefix='')
app.register_blueprint(certify, url_prefix='')

app.register_blueprint(backoffice, url_prefix='')

app.register_blueprint(comments, url_prefix='')

# flask_profiler.init_app(app)


class SQLAlchemyHandler(logging.Handler):

    def emit(self, record):
        trace = None
        exc = record.__dict__['exc_info']
        if exc:
            trace = traceback.format_exc()

        path = request.path
        method = request.method
        ip = request.remote_addr    

        data = {
        		'url':path,
        		'logger_name':record.__dict__['name'],
                'level':record.__dict__['levelname'],
                'context':trace,
                'message':record.__dict__['msg'],
                'created_at':dt.now(),
                'ip_address':ip
            }    
        Log().insert(data)    
        # log = Log(
        #     logger=record.__dict__['name'],
        #     level=record.__dict__['levelname'],
        #     trace=trace,
        #     msg=record.__dict__['msg'],)
        # DB.session.add(log)
        # DB.session.commit()
        return "Some thing went wrong while processing your request. Please try after sometime or get in touch with system administrator."

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ch = SQLAlchemyHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)



loggers = [logger, logging.getLogger('sqlalchemy'), logging.getLogger('flask.app')]

for l in loggers:
    l.addHandler(ch)




# @app.before_request
# def before_request():
#     if request.url.startswith('http://'):
#         print("http")
#         url = request.url.replace('http://', 'https://', 1)
#         code = 301
#         return redirect(url, code=code)
