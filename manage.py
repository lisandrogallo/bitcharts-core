# -*- coding: utf-8 -*-

from bitcharts import app
from bitcharts.scripts.database import manager as database_manager
from bitcharts.scripts.ticker import manager as exchanges_manager
from flask.ext.script import Manager
from flask.ext.script.commands import Clean

# Setup manager (with default commands + clean)
manager = Manager(app)
manager.add_command('clean', Clean)

# Add custom commands
manager.add_command('database', database_manager)
manager.add_command('exchanges', exchanges_manager)

if __name__ == "__main__":
    manager.run()
