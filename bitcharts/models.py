# -*- coding: utf-8 -*-

from bitcharts import db
from bitcharts import parsers
from datetime import date, datetime

PARSERS = {
    'default': parsers.RecursiveKeyFinder(),
    'lanacion': parsers.LaNacion(),
}


class Currency(db.Model):
    __tablename__ = 'currencies'

    id = db.Column(
        db.Integer,
        db.Sequence('currency_id_seq'),
        primary_key=True
    )

    name = db.Column(
        db.String(length=10),
        unique=True
    )

    description = db.Column(db.String(length=25))

    cryptocurrency = db.Column(db.Boolean)

    active = db.Column(db.Boolean)

    def __init__(self, name, description, cryptocurrency, active):
        self.name = name
        self.description = description
        self.cryptocurrency = cryptocurrency
        self.active = active

    def __repr__(self):
        return '<Currency %r>' % self.name


class Exchange(db.Model):
    __tablename__ = 'exchanges'

    id = db.Column(
        db.Integer,
        db.Sequence('exchange_id_seq'),
        primary_key=True
    )

    name = db.Column(db.String(length=20))

    country = db.Column(db.String(length=10))

    parser = db.Column(db.String(length=15))

    url = db.Column(db.String(length=40))

    api = db.Column(db.String(length=40))

    method = db.Column(db.String(length=4))

    key_last = db.Column(db.String(length=30, convert_unicode=True))

    key_buy = db.Column(db.String(length=30, convert_unicode=True))

    route = db.Column(db.String(length=30, convert_unicode=True))

    currency_from_id = db.Column(
        db.Integer,
        db.ForeignKey('currencies.id')
    )

    currency_to_id = db.Column(
        db.Integer,
        db.ForeignKey('currencies.id')
    )

    currency_from = db.relationship(
        'Currency',
        lazy='subquery',
        primaryjoin=(currency_from_id == Currency.id),
    )

    currency_to = db.relationship(
        'Currency',
        lazy='subquery',
        primaryjoin=(currency_to_id == Currency.id),
    )

    active = db.Column(db.Boolean)

    def __init__(self, name, country, parser, url, api, method, key_last,
                 route, key_buy, currency_from_id, currency_to_id, active):
        self.name = name
        self.country = country
        self.parser = parser
        self.url = url
        self.api = api
        self.method = method
        self.key_last = key_last
        self.key_buy = key_buy
        self.route = route
        self.currency_from_id = currency_from_id
        self.currency_to_id = currency_to_id
        self.active = active

    def __repr__(self):
        return '<Exchange %r>' % self.name

    def get_value(self, key):
        parser = PARSERS.get(self.parser, None)
        return parser.execute(self, key)


class Association(db.Model):
    __tablename__ = 'exchanges_currencies'

    id = db.Column(
        db.Integer,
        db.Sequence('association_id_seq'),
        primary_key=True
    )

    exchange_id = db.Column(
        db.Integer,
        db.ForeignKey('exchanges.id')
    )

    last = db.Column(db.Float)

    buy = db.Column(db.Float)

    trend = db.Column(db.String(length=5))

    date = db.Column(
        db.Date,
        default=date.today()
    )

    time = db.Column(
        db.Time,
        default=datetime.now().time()
    )

    def __init__(self, exchange_id, last, buy, trend, date, time):
        self.exchange_id = exchange_id
        self.last = last
        self.buy = buy
        self.trend = trend
        self.date = date
        self.time = time


class Graph(db.Model):
    __tablename__ = 'graphs'

    id = db.Column(
        db.Integer,
        db.Sequence('graphs_id_seq'),
        primary_key=True
    )

    exchange_id = db.Column(
        db.Integer,
        db.ForeignKey('exchanges.id')
    )

    last = db.Column(db.Float)

    opn = db.Column(db.Float)

    close = db.Column(db.Float)

    high = db.Column(db.Float)

    low = db.Column(db.Float)

    volume = db.Column(db.Float)

    date = db.Column(
        db.Date,
        default=date.today()
    )

    time = db.Column(
        db.Time,
        default=datetime.now().time()
    )

    def __init__(self, exchange_id, last, opn, close,
                 high, low, volume, date, time):
        self.exchange_id = exchange_id
        self.last = last
        self.opn = opn
        self.close = close
        self.high = high
        self.low = low
        self.volume = volume
        self.date = date
        self.time = time
