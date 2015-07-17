from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.session import SignedCookieSessionFactory
from pyramid_beaker import session_factory_from_settings
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from lookchic.security import groupfinder

from .models import (
    sess,
    Base
    )

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # initializing DBSession and Base 
    #engine = engine_from_config(settings, 'sqlalchemy.')
    #DBSession.configure(bind=engine)
    #Base.metadata.bind = engine
    config = Configurator(settings=settings)

    # initializing session
    # TODO: turn on the secure=True when using https
    config.include('pyramid_beaker')
    config.set_session_factory(session_factory_from_settings(settings))

    authn_policy = AuthTktAuthenticationPolicy('sosecret', callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    # config = Configurator(settings=settings,
    #                       root_factory='lookchic.models.RootFactory')
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    
    config.include('pyramid_chameleon')
    
    config.add_static_view('static', 'static', cache_max_age=3600)
    
    config.add_route('home', '/')
    config.add_route('post', '/post')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('signup', '/signup')
    config.add_route('add_page', '/add_page/{pagename}')
    config.add_route('edit_page', '/{pagename}/edit_page')
    
    #config.add_route('home', '/')
    config.scan(".views")
    config.scan(".events")
    return config.make_wsgi_app()
