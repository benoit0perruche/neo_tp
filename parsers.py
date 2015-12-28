import csv
from nodes import Dj

class DjsParser():

    def __init__(self, csv_filepath):
        self.csv_filepath = csv_filepath

    def read_csv(self):
        with open(self.csv_filepath) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=",")
            return [Dj(row['id'], row['name'], row['country'], row['sc_url']) for row in reader]