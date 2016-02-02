# -*- coding: utf-8 -*-

from datetime import datetime
from bitcharts.models import Graph
from bitcharts.scripts.utils import active_exchanges
from bitcharts.scripts.utils.helpers import get_alternate_value


def get_exchanges_info():
    """Generate response used by the exchanges API

    Returns:
        DICT: Exchanges info and last value
    """
    now = datetime.now()

    res = {
        '_timestamp': now.strftime('%a %b %d %Y, %H:%M:%S'),
    }

    for exchange in active_exchanges():

        if exchange.key_buy:
            previous = last = buy = trend = None

            # Get the last/buy values and trend computed by the get_values task
            previous = get_alternate_value(exchange, position='previous')
            if previous:
                last, buy, trend = previous

            # Get the last value history from the last 10 days
            query = Graph.query.filter_by(
                exchange_id=exchange.id).order_by(
                Graph.date.desc()).limit(10).all()

            history = []
            for assoc in query:
                history.append(assoc.last)

            key = exchange.name.lower().replace(' ', '_')

            res[key] = {
                'currency': exchange.currency_to.name,
                'buy': buy,
                'sell': last,
                'history': history[::-1],
                'trend': trend or None,
            }

    return res
