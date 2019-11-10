from waitress import serve
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config, view_defaults
from parse_feed import YouTubeParser


def hello_world(request):
    
    print('Incoming request')
    return Response('<body><h1>Hello World!</h1></body>')

@view_defaults(route_name='v1')
class YoutubeParserView(object):
    def __init__(self, request):
        self.request = request

    @view_config(renderer='json')
    def get(self):
        return YouTubeParser.parse_feed_mp3s_list("""https://www.youtube.com/feeds/videos.xml?channel_id=UC4SUWizzKc1tptprBkWjX2Q""", True)

    def post(self):
        return Response('post')

    def delete(self):
        return Response('delete')

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        config.add_route('v1', '/v1')
        config.add_view(YoutubeParserView, renderer='json', attr='get', request_method='GET')
        app = config.make_wsgi_app()
    serve(app, host='0.0.0.0', port=6543)