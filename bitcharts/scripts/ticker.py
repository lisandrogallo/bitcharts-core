# -*- coding: utf-8 -*-

from datetime import date, datetime
from flask.ext.script import Manager
from bitcharts import app, celery
from bitcharts.models import db, Association
from bitcharts.scripts.utils import active_exchanges
from bitcharts.scripts.graphs import get_graphs
from bitcharts.scripts.utils.helpers import timestamp2unix
from bitcharts.scripts.utils.helpers import get_alternate_value
from bitcharts.scripts.utils.helpers import send_email

manager = Manager(usage='Get values and info from active exchanges')


@celery.task(name='bitcharts.send_async_email')
def send_async_email(subject, error_msg):
    send_email(subject, error_msg)


@manager.command
def get_values():
    """
    Manager command to get last values from all active exchanges
    """
    for exchange in active_exchanges():

        ticker = exchange.url + exchange.api
        subject = '[ERROR] %s exchange' % exchange.name
        error_msg = "Exchange: %s\nTicker: %s\nException: " % (exchange.name,
                                                               ticker)

        try:
            previous_last = last = buy = trend = None

            last = exchange.get_value(exchange.key_last)
            if exchange.key_buy:
                buy = exchange.get_value(exchange.key_buy)
            # Close session opened after the execution of get_value method
            db.session.close()

            # Also get previous to calculate trend
            res = get_alternate_value(exchange, position='previous')
            if res:
                previous_last, previous_buy, trend = res

            if previous_last and last:
                if previous_last < last:
                    trend = 'up'
                elif previous_last > last:
                    trend = 'down'
                else:
                    trend = 'equal'

            assoc = Association(
                exchange_id=exchange.id,
                last=last,
                buy=buy,
                trend=trend or None,
                date=date.today(),
                time=datetime.now().time()
            )
            if assoc.last:
                print '%s: %s %s %s' % (exchange.name,
                                        assoc.last,
                                        exchange.currency_to.name,
                                        trend or '')

                db.session.add(assoc)
            else:
                raise Exception

        except Exception as err:
            if not err.message:
                err.message = 'Connection Error. Ticker API is down.'
            print subject + ': ' + str(err.message)
            if app.config.get('ENABLE_MAIL_NOTIFICATIONS', False):
                send_async_email(subject, error_msg + str(err.message))

        finally:
            db.session.commit()
            db.session.close()


@manager.command
def get_graphs_data():
    """
    Manager command to get graph datapoints from all active exchanges
    """
    get_graphs()


def get_avg(exchanges):
    """Calculate average last value from the specified exchanges

    Args:
        exchanges (LIST): Exchanges' names

    Returns:
        FLOAT: Average value
    """
    values = []
    for exchange in active_exchanges():
        exchange_lower = exchange.name.lower().replace(' ', '_')
        if exchange_lower in exchanges:
            res = get_alternate_value(exchange, position='previous')
            if res:
                last, buy, trend = res
                values.append(last)
    avg = reduce(lambda x, y: x + y, values) / len(values)
    return avg


def get_api_ticker():
    """Generate response used by the ticker API

    Returns:
        DICT: Contains average values for ARS and USD exchanges
    """
    exchanges_ars = ['digicoins', 'ripio', 'unisend', 'bitcoin_brothers']
    exchanges_usd = ['la_nacion_blue', 'geeklab', 'infobae_blue']

    now = datetime.now()
    res = {
        '_timestamp': now.strftime('%a %b %d %Y, %H:%M:%S'),
        '_timestamp_unix': timestamp2unix(now),
        'source': 'bitcharts.io',
    }

    try:
        avg_ars = get_avg(exchanges_ars)
        avg_usd = get_avg(exchanges_usd)
        if avg_ars:
            res['last_ars'] = float("{0:.2f}".format(avg_ars))
            if avg_usd:
                res['last_usd'] = float("{0:.2f}".format(avg_ars / avg_usd))

    except Exception, e:
        print e
        res = 'An error has occurred. Try again later.'

    finally:
        return res
