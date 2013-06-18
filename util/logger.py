import json

from util.plot import plot_data

def create_logfile(filename, original_data, processed_data, results):
    """Creates a log file for a graph"""
    fp = open(filename, 'w')

    res_list = [r for r in results]

    data = {'original_data': original_data,
            'processed_data': processed_data,
            'results': res_list }

    json.dump(data, fp)

    fp.close()

def view_logfile(filename):
    """Plots the data from a logfile"""
    fp = open(filename, 'r')

    data = json.load(fp)

    original_data = data['original_data']
    processed_data = data['processed_data']
    results = data['results']

    plot_data(original_data, processed_data, results)

    fp.close()


