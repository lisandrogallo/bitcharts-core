from flask import jsonify
from bitcharts import app
from bitcharts.scripts.calculator import get_calculator
from bitcharts.scripts.exchanges import get_exchanges_info
from bitcharts.scripts.ticker import get_api_ticker
from bitcharts.scripts.graphs import get_api_graphs


@app.route('/exchanges/calculator', methods=['POST'])
def calculator():
    """Bitcharts calculator API

    Returns:
        JSON: Response containing currency values and info from exchanges
    """
    res = jsonify(get_calculator())
    return res


@app.route('/exchanges/info', methods=['POST'])
def exchanges_info():
    """Bitcharts exchanges API

    Returns:
        JSON: Response containing currency values and info from exchanges
    """
    res = jsonify(get_exchanges_info())
    return res


@app.route('/api/ticker', methods=['POST'])
def api_ticker():
    """Bitcharts ticker API

    Returns:
        JSON: Response containing an average BTC value between ARS exchanges
    """
    ticker = get_api_ticker()
    if isinstance(ticker, dict):
        res = jsonify(ticker)
    else:
        res = ticker
    return res


@app.route('/exchanges/graphs/<string:exchange_name>', methods=['POST'])
def api_graphs(exchange_name):
    """Bitcharts graph data API

    Args:
        exchange_name (STRING): Name of the exchange to ask for data

    Returns:
        JSON: Response containing the exchange's close value of each day
    """
    exchange = exchange_name.lower().replace('_', ' ')
    res = get_api_graphs(exchange)
    return res
