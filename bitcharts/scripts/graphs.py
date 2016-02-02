# -*- coding: utf-8 -*-

from flask import request, jsonify
from flask.json import loads
from bitcharts import app, celery
from datetime import date, datetime
from bitcharts.models import db, Exchange, Graph
from bitcharts.scripts.utils import active_exchanges
from bitcharts.scripts.utils.http import get_ticker_response
from bitcharts.scripts.utils.helpers import get_alternate_value
from bitcharts.scripts.utils.helpers import timestamp2js, timestamp2unix
from bitcharts.scripts.utils.helpers import send_email
from requests.exceptions import ConnectionError


@celery.task(name='bitcharts.send_async_email')
def send_async_email(subject, error_msg):
    send_email(subject, error_msg)


def get_graphs():
    """
    Store graph data in database to be used later by the graphs API
    """
    # List of exchanges to store values for a candlesticks graph
    candlesticks_exchanges = ['Bitstamp']

    for exchange in active_exchanges():

        ticker = exchange.url + exchange.api
        subject = '[ERROR] %s exchange (GRAPH)' % exchange.name
        error_msg = "Exchange: %s\nTicker: %s\nException: " % (exchange.name,
                                                               ticker)

        try:

            last = opn = high = low = close = volume = None
            last = exchange.get_value(exchange.key_last)
            # Close session opened after the execution of get_value method
            db.session.close()
            if exchange.name in candlesticks_exchanges:
                # Get the open value (the first value of the day)
                opn, buy, trend = get_alternate_value(exchange,
                                                      position='first')
                # Get ticker to obtain additional values to show in graph
                response = get_ticker_response(exchange)

                if opn and response:

                    # Serialize ticker response
                    json = loads(response.content)

                    close = json['last'] or None,
                    high = json['high'] or None,
                    low = json['low'] or None,
                    volume = float(json['volume']) or None,

        except ConnectionError:
            if not last:
                previous = get_alternate_value(exchange, position='previous')
                if previous:
                    last = previous[0]
                    excep = 'Error connecting with API. Using previous value.'
                    if app.config.get('ENABLE_MAIL_NOTIFICATIONS', False):
                        send_async_email(subject, error_msg + excep)
                else:
                    excep = 'Error connecting with API. No previous value get.'
                    if app.config.get('ENABLE_MAIL_NOTIFICATIONS', False):
                        send_async_email(subject, error_msg + excep)
                print subject + ': ' + excep

        except Exception as err:
            print subject + ': ' + str(err.message)
            if app.config.get('ENABLE_MAIL_NOTIFICATIONS', False):
                send_async_email(subject, error_msg + str(err.message))

        finally:
            try:
                # Write obtained values to database
                graph = Graph(
                    exchange_id=exchange.id,
                    last=last,
                    opn=opn,
                    close=close,
                    high=high,
                    low=low,
                    volume=volume,
                    date=date.today(),
                    time=datetime.now().time()
                )

                if graph.last:
                    print "Getting graph data for '%s'" % exchange.name
                    db.session.add(graph)
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


def get_api_graphs(exchange_name):
    """Generate response used by the graphs API

    Args:
        exchange_name (STRING): Exchange name to lowercase

    Returns:
        JSON: Response containing the exchange's close value of each day
    """
    data = {}

    # Get the Exchange object corresponding to the exchange name provided
    exchange = Exchange.query.filter_by(name=exchange_name).first()

    try:
        # Get all datapoints (datapoint = close value of a day)
        datapoints = Graph.query.filter_by(exchange_id=exchange.id).all()

        # If there are datapoints and 'graph_type' parameter is in the request
        graph = []
        if datapoints and 'graph_type' in request.args:

            # Linear graph
            if request.args['graph_type'] == 'linear':
                for dp in datapoints:
                    date = datetime.combine(dp.date, datetime.min.time())
                    datapoint = {
                        'date': timestamp2js(timestamp2unix(date)),
                        'price': dp.last
                    }
                    graph.append(datapoint)

            # Candlesticks graph
            elif request.args['graph_type'] == 'candlesticks':
                for dp in datapoints:
                    date = datetime.combine(dp.date, datetime.min.time())
                    datapoint = {
                        'date': timestamp2js(timestamp2unix(date)),
                        'open': dp.opn or None,
                        'high': dp.high or None,
                        'low': dp.low or None,
                        'close': dp.close or None,
                        'volume': dp.volume or None
                    }
                    graph.append(datapoint)

        data[exchange_name.replace(' ', '_')] = graph
        return jsonify(data)

    except:
        return 'Error'
