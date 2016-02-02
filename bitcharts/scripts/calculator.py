# -*- coding: utf-8 -*-

from datetime import datetime
from bitcharts.scripts.utils import active_exchanges
from bitcharts.scripts.utils.helpers import get_alternate_value
from bitcharts.scripts.utils.helpers import timestamp2unix


def get_calculator():
    """Generate response used by the calculator API

    Returns:
        DICT: Exchanges info and last value
    """
    now = datetime.now()

    res = {
        '_timestamp': now.strftime('%a %b %d %Y, %H:%M:%S'),
        '_timestamp_unix': timestamp2unix(now)
    }

    for exchange in active_exchanges():

        previous = last = trend = None

        # Get the last value and trend computed by the get_values task
        previous = get_alternate_value(exchange, position='previous')
        if previous:
            last, buy, trend = previous

        key = exchange.name.lower().replace(' ', '_')

        res[key] = {
            'name': exchange.name,
            'url': exchange.url,
            'currency_from': exchange.currency_from.name,
            'currency_to': exchange.currency_to.name,
            'last': last,
            'trend': trend or None,
        }

    return res
