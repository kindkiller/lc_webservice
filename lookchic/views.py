from pyramid.response import Response
from pyramid.request import Request
from pyramid.view import view_config, view_defaults, notfound_view_config

from sqlalchemy.exc import DBAPIError
import mysql.connector
import bcrypt, datetime

import cgi
import re
#from docutils.core import publish_parts

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
)

from .models import (
    sess,
    Userinfo,
    )

from pyramid.view import (
    view_config,
    forbidden_view_config,
    )

from pyramid.security import (
    remember,
    forget,
    )

from .security import USERS

@view_defaults(renderer='json')
class Views:
    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid
    
    # CUSTOM PREDICATES: LOGIN: account verified form confirm/{key}
    def verified(context, request):
        user = sess.query(Userinfo).filter(Userinfo.email==request.POST.get('email')).first()
        if user is None:
            return False
        #elif user.created is None:  
            #return False
        return True
        
    #login 
    @view_config(route_name='login')
    def login(self):
        request = self.request
        #from sys import exc_info
        try:
            a=0
            user = sess.query(Userinfo).filter(Userinfo.Email == request.json_body.get('email')).first() # request.json_body.get('email')).first()
            if user is None:
                a=1
                return Response(json=dict(rc=400, msg="Login Error: no such user"), status_code=400)
            if user.Password == request.json_body.get('password'):
                #user.pwhash == bcrypt.hashpw(bytes(request.POST.get('password'), 'utf-8'), user.salt):
                #request.sess[request.POST.get('email')] = 'sessionstart'
                #request.session.save()
                headers = remember(request, request.json_body.get('email'))
                #headers.append(('X-CSRF-token', request.session.new_csrf_token()))
                a=2
                return Response(headers=headers, json=dict(rc=200, msg="Login: Login Successful", user=user.Email), status_code=200)
    
            sess.remove()
            a=3
            return Response(json=dict(rc=400, msg="Login Error: Email and password don't match"), status_code=400)
        except DBAPIError:
            return Response(conn_err_msg, content_type='text/plain', status_int=400)
        except:
            #print (exc_info())
            return Response(json=dict(rc=400, msg="Login Error: unknown error"), status_code=400)

    #Signup
    @view_config(route_name='signup')
    def signup(self):
        request = self.request

        user = Userinfo()
        user.email = request.json_body.get('email')
        user.pwd = request.json_body.get('password')
        #user.salt = bcrypt.gensalt()
        #user.pwhash = bcrypt.hashpw(bytes(request.POST.get('password'), 'utf-8'), user.salt)
        #user.active = False

        #user.key = bcrypt.hashpw(bytes(request.POST.get('email'), 'utf-8'), bcrypt.gensalt())

        sess.add(user)

        # TODO: replace all try except with trap function from kommons
        #PREDICATE: unique user
        try:
            sess.flush()
        except DBAPIError as e:
            return Response(json=dict(rc=400, msg="Sign up Error: User already signed up"), status_code=400)

        sess.commit()
        sess.remove()
        return Response(json=dict(rc=200, msg="Sign up: Sign up successful"), status_code=200)

    #test
    @view_config(route_name='test')
    def test(self):
        request = self.request
        return Response(json=dict(email=request.json_body.get('email'), pwd=request.json_body.get('password'), msg="Test: TEST API RESPONSE"), status_code=200)

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_lookchic_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

