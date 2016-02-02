# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from celery import Celery
from flask.ext.mail import Mail

# Setup app
app = Flask(__name__)
app.config.from_pyfile('settings.py')

# Setup database
db = SQLAlchemy(app)

# Setup Celery
celery = Celery(
    app.import_name,
    broker=app.config['CELERY_BROKER_URL'],
)
celery.conf.update(app.config)

# Setup mail extension
mail = Mail(app)

# App routes
from bitcharts import views
