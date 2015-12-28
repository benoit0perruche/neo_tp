import csv
from py2neo import Node


class DjsParser():

    def __init__(self, csv_filepath):
        self.csv_filepath = csv_filepath

    def get_djs_countries(self):
        with open(self.csv_filepath) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=",")
            return [(Node("Dj", dj_id=row['dj_id'], name=row['name'], souncloud_url=row['soundcloud_url']), row['country']) for row in reader]


class ClubsParser():

    def __init__(self, csv_filepath):
        self.csv_filepath = csv_filepath

    def get_clubs_countries(self):
        with open(self.csv_filepath) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=",")
            return [(Node("Club", club_id=row['club_id'], name=row['name'], address=row['address']), row['country']) for row in reader]


class EventsParser():

    def __init__(self, csv_filepath):
        self.csv_filepath = csv_filepath

    def get_events_clubs(self):
        with open(self.csv_filepath) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=",")
            return [(Node("Event", event_id=row["event_id"], date=row['date']), row["club_id"])for row in reader]

class DjsEventsParser():

    def __init__(self, csv_filepath):
        self.csv_filepath = csv_filepath

    def get_djs_events(self):
        with open(self.csv_filepath) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=",")
            return [(row['dj_id'], row["event_id"])for row in reader]
