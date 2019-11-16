from waitress import serve
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config, view_defaults
from parse_feed import YouTubeParser
from json import loads


def hello_world(request):
    print('Incoming request')
    return Response('<body><h1>Hello World!</h1></body>')

@view_defaults(route_name='search')
class SearchParserView(object):
    def __init__(self, request):
        self.request = request

    @view_config(renderer='json')
    def get(self):
        s = loads(self.request.body, encoding=self.request.charset)
        return YouTubeParser.search_for_feed(s.get('search_term'))
        

@view_defaults(route_name='feed')
class FeedParserView(object):
    def __init__(self, request):
        self.request = request

    @view_config(renderer='json')
    def get(self):
        return YouTubeParser.parse_feed_mp3s_list("""https://www.youtube.com/feeds/videos.xml?channel_id=UC4SUWizzKc1tptprBkWjX2Q""", True)

    @view_config(renderer='json')
    def post(self):
        s = loads(self.request.body, encoding=self.request.charset)
        return YouTubeParser.parse_feed_mp3s_list(s.get('feed_url'), True)

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        config.add_route('feed', '/v1/feed')
        config.add_view(FeedParserView, renderer='json', attr='get', request_method='GET')
        config.add_view(FeedParserView, renderer='json', attr='post', request_method='POST')
        config.add_route('search', '/v1/search')
        config.add_view(SearchParserView,  renderer='json',attr='post', request_method='POST')
        app = config.make_wsgi_app()
    serve(app, host='0.0.0.0', port=6543)