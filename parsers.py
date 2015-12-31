import csv
from py2neo import Node


class DjsParser():

    def __init__(self, csv_filepath):
        self.csv_filepath = csv_filepath

    def get_djs_countries(self):
        with open(self.csv_filepath) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=",")
            return [(Node("Dj", dj_id=row['dj_id'], name=row['name'], souncloud_url=row['soundcloud_url'], soundcloud_id=row['soundcloud_id']), row['country']) for row in reader]


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
            return [(Node("Event", event_id=row["event_id"]), row["club_id"], row['date']) for row in reader]


class DjsEventsParser():

    def __init__(self, csv_filepath):
        self.csv_filepath = csv_filepath

    def get_djs_events(self):
        with open(self.csv_filepath) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=",")
            return [(row['dj_id'], row["event_id"])for row in reader]


class TrackParser():

    def __init__(self, csv_filepath):
        self.csv_filepath = csv_filepath

    def get_events_clubs(self):
        with open(self.csv_filepath) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=",")
            return [(Node("Track",
                          title=row["title"],
                          duration=row['duration'],
                          playback_count=row['playback_count'],
                          permalink=row['permalink'],
                          ), row["dj_id"], row['release_date'])for row in reader]


class BoilerRoomParser():

    def __init__(self, csv_filepath):
        self.csv_filepath = csv_filepath

    def get_boiler_djs(self):
        with open(self.csv_filepath) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=",")
            return [(Node("BoilerRoom",
                          id=row['br_id'],
                          title=row["title"],
                          view_count=row['view_count'],
                          like_count=row['like_count'],
                          permalink='http://www.youtube.com/watch?v='+row['br_id'],
                          ), row["dj_id"], row['published_date'])for row in reader]


class TopParser():

    def __init__(self, csv_filepath):
        self.csv_filepath = csv_filepath

    def get_top(self):
        with open(self.csv_filepath) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=",")

            return [(row['rank'][:-1], row['dj_name'].lower()) for row in reader]