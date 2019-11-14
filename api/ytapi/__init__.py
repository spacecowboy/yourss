"""Main entry point"""
from pyramid.config import Configurator
import os

def main(global_config, **settings):
    settings = {k: os.path.expandvars(v) for k, v in settings.items()}
    settings['pyramid.debug'] = True
    config = Configurator(
        settings=settings, debug_logger='pyramid.debug'
    )
    # config.add_renderer('json')
    # config.include('yt-api.resources')
    # config.scan('yt-api.api')
    return config.make_wsgi_app()