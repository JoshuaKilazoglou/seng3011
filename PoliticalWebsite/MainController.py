from flask_restful import Resource, reqparse
from PoliticalWebsite.Services.EventService import EventService
from PoliticalWebsite.Services.SectorService import SectorService


class Events(Resource):
    def __init__(self):
        self.event_service = EventService()

    def get(self):
        return self.event_service.get_all_events(), 200


class Sectors(Resource):
    def __init__(self):
        self.sector_service = SectorService()

    def get(self):
        return self.sector_service.get_all_sectors(), 200


class NewsArticles(Resource):
    def get(self):
        return {
            'articles':
            [
                {
                    'headline': 'headline1',
                    'text': 'text1'
                },
                {
                    'headline': 'headline2',
                    'text': 'text2'
                }
            ]

        }, 200


class GraphData(Resource):
    def get(self):
        return {
            'pre_event': [0.4, 0.5, 0.2, 0.5, 0.6, 0.1, 0.7],
            'post_event': [0.3, 0.7, 0.3, 0.2, 0.4, 0.9, 0.1]
        }, 200