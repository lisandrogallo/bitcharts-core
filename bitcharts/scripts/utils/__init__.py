# -*- coding: utf-8 -*-

from bitcharts.models import Exchange, Currency
from sqlalchemy.sql import func

_registry = None


def active_exchanges(name=None, random=False):
    global _registry

    active_exchanges_query = Exchange.query.filter_by(
                active=True).join(Currency, Exchange.currency_from).filter_by(
                active=True)

    if _registry is None:
        if not name:
            _registry = active_exchanges_query.all()
        elif random:
            _registry = active_exchanges_query.filter_by(
                name=name).order_by(func.random()).first()
        else:
            _registry = active_exchanges_query.filter_by(name=name).all()

    return _registry
