from pyramid.view import view_config, view_defaults
from cornice.resource import resource
from collections import defaultdict

from pyramid.exceptions import Forbidden
from pyramid.security import authenticated_userid, effective_principals

from cornice import Service
from json import loads
from parse_feed import YouTubeParser

@resource(name='search', path='/search')
class SearchParserView(object):
    def __init__(self, request, context=None): # Context parameter required by cornice
        self.request = request

    def get(self):
        search_term = "Majority Report"
        return YouTubeParser.search_for_feed(search_term)
        

@resource(name='feed', path='/feed')
class FeedParserView(object):
    def __init__(self, request, context=None):
        self.request = request

    # TODO: parse_feed can raise a ValueError from an invalid URL. Need to create a schema instaed
    def get(self):
        return YouTubeParser.parse_feed_mp3s_list("""https://www.youtube.com/feeds/videos.xml?channel_id=UC4SUWizzKc1tptprBkWjX2Q""", True)

    def post(self):
        s = loads(self.request.body, encoding=self.request.charset)
        return YouTubeParser.parse_feed_mp3s_list(s.get('feed_url'), True)