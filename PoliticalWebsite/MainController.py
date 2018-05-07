from flask_restful import Resource, reqparse
from PoliticalWebsite.Services.EventService import EventService
from PoliticalWebsite.Services.SectorService import SectorService
from PoliticalWebsite.Services.GraphService import GraphService
from PoliticalWebsite.Services.PostSentimentService import PostSentimentService
from PoliticalWebsite.Services.NewsService import NewsService
from datetime import datetime
import sys


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
    def __init__(self):
        self.news_service = NewsService()

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('query', type=str)
        self.parser.add_argument('date', type=str)

    def get(self):
        args = self.parser.parse_args()

        query = args['query']
        date_string = args['date']

        date = datetime.strptime(date_string, '%Y-%m-%d')

        return self.news_service.get_news_response(query, date), 200


class GraphData(Resource):
    def __init__(self):
        self.graph_service = GraphService()

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('sector', type=str)
        self.parser.add_argument('date', type=str)

    def get(self):
        args = self.parser.parse_args()

        sector = args['sector']
        date_string = args['date']

        date = datetime.strptime(date_string, '%Y-%m-%d')

        return self.graph_service.get_graph_data_by_sector(sector, date), 200


class PostSentiment(Resource):
    def __init__(self):
        self.post_sentiment_service = PostSentimentService()

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('sector', type=str)
        self.parser.add_argument('date', type=str)

    def get(self):
        args = self.parser.parse_args()

        sector = args['sector']
        date_string = args['date']

        date = datetime.strptime(date_string, '%Y-%m-%d')

        return self.post_sentiment_service.get_sentiment_by_sector(sector, date), 200











