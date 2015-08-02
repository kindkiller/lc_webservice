from pyramid.interfaces import IRequest
from pyramid.interfaces import IRootFactory
from pyramid.interfaces import IRoutesMapper
from pyramid.interfaces import IRouteRequest
from pyramid.interfaces import ITraverser
from pyramid.interfaces import IViewClassifier
from pyramid.interfaces import IView
from pyramid.traversal import DefaultRootFactory
from pyramid.traversal import ResourceTreeTraverser
from pyramid.view import view_config
from zope.interface import providedBy
import logging

log = logging.getLogger(__name__)

@view_config(name="options_view", request_method='OPTIONS', route_name='options')
class OptionsView(object):
    
    all_methods = set(['GET', 'HEAD', 'POST', 'OPTIONS', 'PUT', 'DELETE', 'PATCH', 'TRACE'])
    
    def _get_view_predicates(self, view_callable):
        # hack
        view_predicates = view_callable.func_dict.get('__predicates__', [])
            
        return view_predicates
    
    def _get_allowed_methods_from_predicates(self, predicates):
        allowed_methods = set(list(self.all_methods)[:])
        for p in predicates:
            # hack
            predicate = getattr(p, '__text__', '')
            if predicate.startswith('request method = '):
                allowed_methods &= set(eval(predicate[17:]))
        
        return allowed_methods
    
    def __init__(self, request):
        self.request = request
        
    def __call__(self):
        request = self.request
        reg = request.registry
        default_root_factory = reg.queryUtility(IRootFactory, default=DefaultRootFactory)
        mapper = reg.getUtility(IRoutesMapper)
        path_info = '/'.join(request.matchdict['path'])
        if path_info[:1] != '/':
            path_info = '/' + path_info
        
        matched_routes = []
        for route in mapper.get_routes():
            if route is request.matched_route:
                # Don't match ourself
                continue
            if route.match(path_info) is not None:
                matched_routes.append(route)
                    
        allowed_methods = set(['OPTIONS']) # We're already doing OPTIONS on it
        for route in matched_routes:
            route_predicates = getattr(route, 'predicates', [])
            route_allowed_methods = self._get_allowed_methods_from_predicates(route_predicates)
                
            request_iface = reg.queryUtility(
                IRouteRequest,
                name=route.name,
                default=IRequest)
                
            root_factory = route.factory or default_root_factory
            root = root_factory(route)
            traverser = reg.adapters.queryAdapter(root, ITraverser)
            if traverser is None:
                traverser = ResourceTreeTraverser(root)
                
            tdict = traverser(request)
            
            view_callable = reg.adapters.lookup(
                (IViewClassifier, request_iface, providedBy(tdict['context'])),
                IView, name=tdict['view_name'], default=None
                )
            
            view_predicates = self._get_view_predicates(view_callable)
            view_allowed_methods = self._get_allowed_methods_from_predicates(view_predicates)
            
            allowed_methods |= route_allowed_methods & view_allowed_methods
        
        request.response.headers['Allow'] = ', '.join(allowed_methods)
        
        if 'Access-Control-Request-Method' in request.headers:
            request.response.headers['Access-Control-Allow-Methods'] = ', '.join(allowed_methods)

        return request.response
