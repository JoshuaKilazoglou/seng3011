import jsonpickle
import os
import sys
from settings import APP_ROOT


class SectorService:

    def get_all_sectors(self):
        path = os.path.join(APP_ROOT, 'PoliticalWebsite', 'Data', 'Sectors.json')
        with open(path) as eventsJson:
            return jsonpickle.decode(eventsJson.read())
