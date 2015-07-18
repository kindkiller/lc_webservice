from pyramid.response import Response
from pyramid.request import Request
from pyramid.view import view_config, view_defaults, notfound_view_config

from sqlalchemy.exc import DBAPIError
import mysql.connector
import bcrypt, datetime

import os
import uuid
import shutil

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
        from sys import exc_info
        try:
            user = sess.query(Userinfo).filter(Userinfo.Email == request.json_body.get('email')).first() # request.json_body.get('email')).first()
            if user is None:
                return Response(json=dict(rc=400, msg="Login Error: no such user"), status_code=400)
            if user.Password == request.json_body.get('password'):
                #user.pwhash == bcrypt.hashpw(bytes(request.POST.get('password'), 'utf-8'), user.salt):
                #request.sess[request.POST.get('email')] = 'sessionstart'
                #request.session.save()
                headers = remember(request, request.json_body.get('email'))
                #headers.append(('X-CSRF-token', request.session.new_csrf_token()))
                return Response(headers=headers, json=dict(rc=200, msg="Login: Login Successful", user=user.Email), status_code=200)
    
            sess.remove()
            return Response(json=dict(rc=400, msg="Login Error: Email and password don't match"), status_code=400)
        except DBAPIError:
            return Response(conn_err_msg, content_type='text/plain', status_int=400)
        except:
            print (exc_info())
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

    #save a posted image
    @view_config(route_name='post')
    def post(self):
        request = self.request
        from sys import exc_info
        # ``filename`` contains the name of the file in string format.
        #
        # WARNING: this example does not deal with the fact that IE sends an
        # absolute file *path* as the filename.  This example is naive; it
        # trusts user input.
        try:
            filename = request.POST['file'].filename

            # ``input_file`` contains the actual file data which needs to be
            # stored somewhere.
            if (filename):
                input_file = request.POST['file'].file

                # strip leading path from file name to avoid directory traversal attacks
                fn = os.path.basename(filename)
                #open('../static/img/' + fn, 'wb').write(input_file.file.read())

                # Note that we are generating our own filename instead of trusting
                # the incoming filename since that might result in insecure paths.
                # Please note that in a real application you would not use /tmp,
                # and if you write to an untrusted location you will need to do
                # some extra work to prevent symlink attacks.

                file_path = os.path.join('C:\\virtualenvs\\lc_env\\lookchic\\lookchic\\static\\img', '%s' % uuid.uuid4() + '.' + fn.rpartition('.')[2])

                # We first write to a temporary file to prevent incomplete files from
                # being used.

                temp_file_path = file_path + '~'

                # Finally write the data to a temporary file
                input_file.seek(0)
                with open(temp_file_path, 'wb') as output_file:
                    shutil.copyfileobj(input_file, output_file)

                # Now that we know the file has been fully saved to disk move it into place.

                os.rename(temp_file_path, file_path)

                return Response(json=dict(rc=200, msg="File uploaded"), status_code=200)
            else:
                return Response(json=dict(rc=400, msg="no file name"), status_code=400)
        except:
            print (exc_info())
            return Response(json=dict(rc=400, msg="Login Error: unknown error"), status_code=400)

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

