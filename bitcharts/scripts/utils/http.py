# -*- coding: utf-8 -*-

import warnings
from requests import get, post, codes
from requests.packages.urllib3 import exceptions
from bitcharts.scripts.utils.decorators import retry
from requests.exceptions import ConnectionError, Timeout, HTTPError


@retry((ConnectionError, Timeout, HTTPError))
def get_ticker_response(exchange):

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
    }

    ticker_url = exchange.url + exchange.api

    # Disable annoying urllib3 warnings
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', exceptions.InsecureRequestWarning)

        response = None

        if exchange.method == 'POST':
            response = post(ticker_url, verify=False)
        if exchange.method == 'GET' or response.status_code != codes.ok:
            response = get(ticker_url, headers=headers, verify=False)

        return response
