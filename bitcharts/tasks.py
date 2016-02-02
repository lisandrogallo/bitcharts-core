from bitcharts import celery
from bitcharts.scripts.ticker import get_values as cmd_get_values
from bitcharts.scripts.ticker import get_graphs_data as cmd_get_graphs_data

@celery.task(name='bitcharts.get_values')
def get_values():
    cmd_get_values()


@celery.task(name='bitcharts.get_graphs_data')
def get_graphs_data():
    cmd_get_graphs_data()
