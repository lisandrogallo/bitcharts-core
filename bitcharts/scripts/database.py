# -*- coding: utf-8 -*-

from ast import literal_eval
from bitcharts import app
from bitcharts.models import db, Currency, Exchange
from bitcharts.scripts.utils.config_parser import config_parser
from flask.ext.script import Manager, prompt_bool

# Manager to handle commands related to database operations
manager = Manager(usage='Perform database operations')

# Get paths for configuration files
exchanges = app.config.get('EXCHANGES_FILE', False)
currencies = app.config.get('CURRENCIES_FILE', False)


@manager.command
def create(exchanges_file=exchanges, currencies_file=currencies):
    """Creates database schema from SQLAlchemy models

    Args:
        exchanges_file (STRING, optional): Path to file with exchanges info
        currencies_file (STRING, optional): Path to file with currencies info
    """
    # Create database from squema defined in models.py
    db.create_all()

    # Parse configuration file and load currencies data in database
    currencies = config_parser(currencies_file)
    for key, value in currencies.iteritems():
        currency = Currency(
            name=key,
            description=value['description'],
            cryptocurrency=literal_eval(value['cryptocurrency']),
            active=literal_eval(value['active'])
        )

        db.session.add(currency)
    db.session.commit()

    # Parse configuration file and load exchanges data in database
    exchanges = config_parser(exchanges_file)
    for key, value in exchanges.iteritems():
        currency_from = Currency.query.filter_by(
            name=value['currency_from']).first()

        currency_to = Currency.query.filter_by(
            name=value['currency_to']).first()

        exchange = Exchange(
            name=key,
            country=value['country'],
            parser=value['parser'],
            url=value['url'],
            api=value['api'],
            method=value['method'],
            key_last=value['key_last'].decode('utf-8'),
            key_buy=value['key_buy'].decode('utf-8') if 'key_buy' in value else None,
            route=value['route'].decode('utf-8') if 'route' in value else None,
            currency_from_id=currency_from.id,
            currency_to_id=currency_to.id,
            active=literal_eval(value['active'])
        )

        db.session.add(exchange)
    db.session.commit()


@manager.command
def rebuild():
    "Recreates database tables"
    if prompt_bool('Are you sure you want to rebuild database?'):
        db.drop_all()
        create()
