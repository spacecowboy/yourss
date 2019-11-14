"""Main entry point"""
"""pserve development.ini --reload"""
from pyramid.config import Configurator
import os
from pyramid.security import Everyone, Authenticated, Allow

def main(global_config, **settings):
    settings = {k: os.path.expandvars(v) for k, v in settings.items()}
    settings['pyramid.debug'] = True
    config = Configurator(
        settings=settings, root_factory=Root
    )
    # config.include('ytapi.resources')
    # resource.add_view(User.get)
    config.include('cornice') # Otherwise attributeerror when adding cornice
    config.scan("ytapi.resources")
    return config.make_wsgi_app()


class Root(object):
    __acl__ = [
        (Allow, Everyone, "view"),
        (Allow, Authenticated, "authenticated"),
    ]

    def __init__(self, request):
        self.request = request