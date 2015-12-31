from datetime import timedelta, date
from parsers import BoilerRoomParser, ClubsParser, DjsEventsParser, DjsParser, EventsParser, TopParser, TrackParser
from py2neo import authenticate, cypher, error, Graph, GraphError, Node, Relationship


def define_constraints():
    try:
        graph.schema.create_uniqueness_constraint("Dj", "dj_id")

    except GraphError as error:
        print error

    try:
        graph.schema.create_uniqueness_constraint("Country", "name")
    except GraphError as error:
        print error

    try:
        graph.schema.create_uniqueness_constraint("Club", "ra_id")
    except GraphError as error:
        print error

    try:
        graph.schema.create_uniqueness_constraint("Event", "event_id")
    except GraphError as error:
        print error

    try:
        graph.schema.create_uniqueness_constraint("Track", "permalink")
    except GraphError as error:
        print error

    try:
        graph.schema.create_uniqueness_constraint("Day", "date")
    except GraphError as error:
        print error

    try:
        graph.schema.create_uniqueness_constraint("Top100", "Year")
    except GraphError as error:
        print error

def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def create_day_nodes(year):
    first_date = date(year, 1, 1)
    last_date = date(year, 12, 31)

    for single_date in date_range(first_date, last_date):
        graph.create(Node('Day', date=single_date.strftime("%Y-%m-%d")))


def create_djs_countries(csv_file):
    djs_parser = DjsParser(csv_file)

    for dj_node, country in djs_parser.get_djs_countries():
        try:
            dj_lives_in_country = Relationship(dj_node, "LIVES_IN", graph.merge_one("Country", "name", country))
            graph.create(dj_lives_in_country)
        except cypher.CypherError as error:
            print error


def create_clubs_countries(csv_file):
    clubs_parser = ClubsParser(csv_file)

    for club_node, country in clubs_parser.get_clubs_countries():
        try:
            clubs_is_in_country = Relationship(club_node, "IS_IN", graph.merge_one("Country", "name", country))
            graph.create(clubs_is_in_country)
        except cypher.CypherError as error:
            print error


def create_events_clubs(csv_file):
    events_parser = EventsParser(csv_file)

    for event_node, club_id, event_date in events_parser.get_events_clubs():
        try:
            club_hosted_event = Relationship(graph.merge_one("Club", "club_id", club_id), "HOSTED", event_node)
            graph.create(club_hosted_event)

            event_happened_day = Relationship(event_node, "HAPPENED", graph.merge_one("Day", "date", event_date))
            graph.create(event_happened_day)

        except cypher.CypherError as error:
            print error


def create_djs_events(csv_file):
    djs_events_parser = DjsEventsParser(csv_file)

    for dj_id, event_id in djs_events_parser.get_djs_events():
        try:
            dj_played_at_event = Relationship(graph.merge_one("Dj", "dj_id", dj_id), "PLAYED_AT", graph.merge_one("Event", "event_id", event_id))
            graph.create(dj_played_at_event)
        except cypher.CypherError as error:
            print error


def create_djs_tracks(csv_file):
    track_parser = TrackParser(csv_file)

    for track_node, dj_id, release_date in track_parser.get_events_clubs():
        try:
            dj_produced_track = Relationship(graph.merge_one("Dj", "dj_id", dj_id), "PRODUCED", track_node)
            graph.create(dj_produced_track)

            track_released_day = Relationship(track_node, "RELEASED", graph.merge_one("Day", "date", release_date))
            graph.create(track_released_day)

        except cypher.CypherError as error:
            print error


def create_djs_boilers(csv_file):
    boiler_parser = BoilerRoomParser(csv_file)

    for boiler_node, dj_id, boiler_date in boiler_parser.get_boiler_djs():
        try:
            dj_played_at_boiler = Relationship(graph.merge_one("Dj", "dj_id", dj_id), "PLAYED_AT", boiler_node)
            graph.create(dj_played_at_boiler)

            boiler_happened_day = Relationship(boiler_node, "HAPPENED", graph.merge_one("Day", "date", boiler_date))
            graph.create(boiler_happened_day)

        except cypher.CypherError as error:
            print error


def create_top(csv_file):
    top_parser = TopParser(csv_file)
    for rank, dj_name in top_parser.get_top():
        result_dj = graph.find_one("Dj", property_key='name', property_value=dj_name)
        if result_dj is not None:
            dj_featured_top = Relationship(result_dj, "FEATURED_IN", graph.merge_one('Top100', 'year', 2015), rank=rank)
            graph.create(dj_featured_top)


def create_indexes():
    graph.schema.create_index("Day", "date")
    graph.schema.create_index("Club", "name")
    graph.schema.create_index("Dj", "name")
    graph.schema.create_index("Track", "playback_count")
    graph.schema.create_index("BoilerRoom", "view_count")

if __name__ == '__main__':
    print "By default the connection is made to the graph on http://127.0.0.1:7474/db/data/"

    username = raw_input('Enter your neo4j username: ')
    password = raw_input('Enter your neo4j password: ')

    try:
        authenticate("127.0.0.1:7474", username, password)
        graph = Graph("http://127.0.0.1:7474/db/data/")

        define_constraints()
        try:
            create_day_nodes(2015)
            create_djs_countries("raw_data/djs.csv")
            create_clubs_countries("raw_data/clubs.csv")
            create_events_clubs("raw_data/events.csv")
            create_djs_events("raw_data/djs_events.csv")
            create_djs_tracks("raw_data/tracks.csv")
            create_djs_boilers("raw_data/brs.csv")
            create_top("raw_data/top100.csv")
            create_indexes()
        except GraphError as e:
            print e

    except SystemError or error.Unauthorized:
        "There was a problem with your credentials please retry"

