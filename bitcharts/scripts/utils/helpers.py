# -*- coding: utf-8 -*-

from datetime import datetime
from bitcharts.models import Association
from flask.ext.mail import Message
from bitcharts import app, mail


def get_alternate_value(exchange, position, today=datetime.now().date()):
    if position == 'previous':
        order = Association.time.desc()
    elif position == 'first':
        order = Association.time.asc()

    res = Association.query.filter_by(
          exchange_id=exchange.id).filter_by(
          date=today).order_by(order).first()

    if res:
        if exchange.key_buy:
            return [res.last, res.buy, res.trend]
        else:
            return [res.last, None, res.trend]
    else:
        return None


def timestamp2unix(timestamp, epoch=datetime(1970, 1, 1)):
    udt = timestamp - epoch
    return udt.total_seconds()


def timestamp2js(unix_timestamp):
    return round(unix_timestamp, 0) * 1000


def send_email(subject, error_msg):
    """Background task to send an email with Flask-Mail.

    Args:
        subject (STRING): Subject of mail message
        error_msg (STRING): Error message to include in mail body
    """
    with app.app_context():
        msg = Message(subject,
                      sender=app.config.get('MAIL_USERNAME', False),
                      recipients=app.config.get('ADMINS', False),)
        msg.body = error_msg
        msg.html = None
        mail.send(msg)
