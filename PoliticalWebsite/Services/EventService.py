import jsonpickle
import os
import sys
from settings import APP_ROOT


class EventService:

    def get_all_events(self):
        path = os.path.join(APP_ROOT, 'PoliticalWebsite', 'Data', 'Events.json')
        with open(path) as eventsJson:
            return jsonpickle.decode(eventsJson.read())
