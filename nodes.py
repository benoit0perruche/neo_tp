class Country:

    def __init__(self, name):
        self.name = name


class Dj:

    def __init__(self, dj_id, name, country, soundcloud_url):
        self.dj_id = dj_id
        self.name = name
        self.country = country
        self.soundcloud_url = soundcloud_url


class Venue:

    def __init__(self, venue_id, name, address, country):
        self.venue_id = venue_id
        self.name = name
        self.address = address
        self.country = country