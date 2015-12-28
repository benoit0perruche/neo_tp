from parsers import ClubsParser, DjsEventsParser, DjsParser, EventsParser
from py2neo import authenticate, cypher, Graph, GraphError, Relationship, schema


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

    for event_node, club_id in events_parser.get_events_clubs():
        try:
            club_hosted_event = Relationship(graph.merge_one("Club", "club_id", club_id), "HOSTED", event_node)
            graph.create(club_hosted_event)
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

if __name__ == '__main__':
    authenticate("127.0.0.1:7474", "neo4j", "neotp")
    graph = Graph("http://127.0.0.1:7474/db/data/")

    define_constraints()
    create_djs_countries("raw_data/djs.csv")
    create_clubs_countries("raw_data/clubs.csv")
    create_events_clubs("raw_data/events.csv")
    create_djs_events("raw_data/djs_events.csv")


