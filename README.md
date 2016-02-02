Bitcharts Core
==============

Core and scripts used on http://bitcharts.io

## Installation

### Dependencies

    sudo pip install -r requirements.txt

If you don't have Pip, find it here: http://pypi.python.org/pypi/pip

### Edit configuration file

Edit the **bitcharts/settings.py** file to set database connection string parameters, Celery broker configuration and mail settings for notifications.

```python
# Database settings
MYSQL_USERNAME = ''
MYSQL_PASSWORD = ''
MYSQL_HOSTNAME = 'localhost'
MYSQL_PORT = '3306'
MYSQL_DATABASE = 'bitcharts'

# Celery settings
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TIMEZONE = 'America/Argentina/Buenos_Aires'

# Email notifications
ENABLE_MAIL_NOTIFICATIONS = False
MAIL_SERVER = ''
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
ADMINS = ['admin@domain.com']
```

### Initialize database

    python manage database create

### Running development server

    python manage.py runserver

### Running tasks queue

    celery -B --app=bitcharts.celery worker --concurrency=2 --loglevel=info

## Credits

**Author:** Lisandro Gallo (@lisogallo) liso [at] riseup.net

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see http://www.gnu.org/licenses/.

-----
<p align="center">
<img alt="Bitcoin" title="Donate with Bitcoin" src="http://mw.gg/i/bitcoin.png" /> 1CPb9QZBkz3gD1rvG9ekNFK5k6jpUycika
</p>
