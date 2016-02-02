# -*- coding: utf-8 -*-

from json import loads
from requests import codes
from bitcharts.scripts.utils.http import get_ticker_response

__all__ = [
    'RecursiveKeyFinder',
    'LaNacion',
]


class RecursiveKeyFinder():

    def execute(self, exchange, key):
        """Search the ticker response recursively for the key specified

        Args:
            exchange (OBJECT): Exchange object

        Returns:
            FLOAT: Value for the key specified
        """
        res = None
        # Request the ticker and get the HTTP response
        response = get_ticker_response(exchange)
        if response:
            # Deserialize the response content
            data = self._deserialize(response)

            if data:
                # If the route to key is set on the exchange configuration
                if exchange.route:
                    route = exchange.route
                    route = route.split(',')
                    res = self._search_by_key_route(data, *route)
                # If the route is not set then search for the key directly
                else:
                    res = self._search_by_key(data, key)

        return res

    def _search_by_key(self, data, key):
        """Search for the key specified and get the value

        Args:
            data (DICT): Ticker response deserialized
            key (STRING): Key to search which contains the desired value

        Returns:
            FUNCTION or FLOAT: The function calls itself recursively
            until it finds the specified key or returns the value in float
        """
        if isinstance(data, dict):
            if key in data:
                if not isinstance(data.get(key), dict):
                    value = data.get(key)
                    if isinstance(value, str) or isinstance(value, unicode):
                        value = value.replace(',', '.')
                    return float("{0:.2f}".format(float(value)))

            # If key is not in 'data' itself, search inside each 'data' element
            else:
                # Search on each element until key is found
                for v in data.itervalues():
                    res = self._search_by_key(v, key)
                    if res:
                        return res

        # If 'data' is not a dictionary search again, but now inside 'data'
        elif isinstance(data, list):
            return self._search_by_key(data[0], key)

    def _search_by_key_route(self, data, *args):
        """Search for the key along the route specified and get the value

        Args:
            data (DICT): Ticker response deserialized
            *args: All the keys composing the route

        Returns:
            FLOAT: The value for the found key
        """
        for count, key in enumerate(args):
            key = key.strip()
            # If key in 'data' then get a new dict or the desired value
            if key in data:
                data = data.get(key)

        if isinstance(data, str) or isinstance(data, unicode):
            data = data.replace(',', '.')

        return float("{0:.2f}".format(float(data)))

    def _deserialize(self, response):
        """Deserialize response content obtained from ticker

        Args:
            response (OBJECT): HTTP response

        Returns:
            DICT: JSON deserialized
        """
        if response.status_code == codes.ok:
            return loads(response.content)


class LaNacion(RecursiveKeyFinder):

    def _deserialize(self, response):
        if response.status_code == codes.ok:
            return loads(response.content[19:-2])
