from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.session import SignedCookieSessionFactory
from pyramid_beaker import session_factory_from_settings
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from lookchic.security import groupfinder


from pyramid.request import Request
from pyramid.request import Response

def request_factory(environ):
    request = Request(environ)
    #if request.is_xhr:
    #if request.method == 'OPTIONS':
    request.response = Response()
    #request.response.headerlist = []
    request.response.headerlist.extend(
        (
            ("Access-Control-Allow-Origin", "http://localhost:8000"),
            #("Access-Control-Allow-Methods", "GET, PUT, POST, DELETE"),
            #("Access-Control-Expose-Headers", "Authorization"),
            #("Access-Control-Allow-Credentials", 'true'),
            ("Access-Control-Allow-Headers", "Authorization")
        )
    )
    return request



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

    config.set_request_factory(request_factory)

    #config.add_route('home', '/')

    config.add_route('post', '/post')
    config.add_route('login', '/login')

    config.add_route('signup', '/signup')
    config.add_route('main', '/main')
    config.add_route('search', '/search')
    config.add_route('logout', '/logout')


    #config.add_route('add_page', '/add_page/{pagename}')
    #config.add_route('edit_page', '/{pagename}/edit_page')
    
    #config.add_route('home', '/')

    #config.scan(".utility_views")
    config.scan(".views")
    #config.scan(".events")

    return config.make_wsgi_app()
