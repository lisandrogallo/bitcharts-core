import os
from celery.schedules import crontab

# App settings
EXCHANGES_FILE = 'config/exchanges.cfg'
CURRENCIES_FILE = 'config/currencies.cfg'

# Database settings
MYSQL_USERNAME = ''
MYSQL_PASSWORD = ''
MYSQL_HOSTNAME = 'localhost'
MYSQL_PORT = '3306'
MYSQL_DATABASE = 'bitcharts'
SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s' % (MYSQL_USERNAME,
                                                      MYSQL_PASSWORD,
                                                      MYSQL_HOSTNAME,
                                                      MYSQL_PORT,
                                                      MYSQL_DATABASE)

# Celery settings
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_SERIALIZER = 'json'
CELERY_IMPORTS = ('bitcharts.tasks', )
CELERY_TIMEZONE = 'America/Argentina/Buenos_Aires'

# Celery schedules settings
CELERYBEAT_SCHEDULE = {
    'get-values-every-5-minutes': {
        'task': 'bitcharts.get_values',
        'schedule': crontab(minute='*/1'),
    },
    'get-values-at-midnight': {
        'task': 'bitcharts.get_graphs_data',
        'schedule': crontab(hour=23, minute=55),
    },
}

# Email notifications
ENABLE_MAIL_NOTIFICATIONS = False
MAIL_SERVER = ''
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
ADMINS = ['admin@domain.com']
