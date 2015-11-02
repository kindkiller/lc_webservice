import os
import uuid
import shutil

from pyramid.request import Response
from pyramid.view import view_defaults
from sqlalchemy.exc import DBAPIError
import bcrypt
from Authentication import generateToken,authenticateUser

from .models import (
    Userinfo,
    )

from pyramid.view import (
    view_config,
)

from sys import exc_info

from dbconnection import Session
sess=Session()

import postevents
import json

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
    @view_config(route_name='login', request_method='OPTIONS')
    def login_options(self):
        resp = self.request.response
        return resp

    @view_config(route_name='login',  request_method='POST')
    def login(self):
        request = self.request
        resp = request.response
        try:
            user = sess.query(Userinfo).filter(Userinfo.Email ==request.json_body.get('email')).first() # request.POST.get('email')).first() # request.json_body.get('email')).first()
            if user is None:
                return Response(json=dict(rc=400, msg="Login Error: no such user"), status_code=400)
            if user.Password == request.json_body.get('password'): #request.POST.get('password'):
                #user.pwhash == bcrypt.hashpw(bytes(request.POST.get('password'), 'utf-8'), user.salt):
                #request.sess[request.POST.get('email')] = 'sessionstart'
                #request.session.save()
                #headers = remember(request, request.json_body.get('email'))
                #headers.append(('X-CSRF-token', request.session.new_csrf_token()))
                userSecreat=user.Salt
                userid=user.ID
                userToken=generateToken(userid,user.Password)
                resp.status_code = 200
                #(json=dict(rc=200, msg="Login Successful", user=user.Email, userid=user.ID), status_code=200)
                #resp.headerlist.append(('Access-Control-Allow-Origin', '*'))
                return dict(rc=200, msg="Login Successful", user=user.Email, userid=user.ID, accessToken=userToken)

            #sess.remove()
            #resp.status_code = 400
            return resp(json=dict(rc=400, msg="Login Error: Email and password don't match"), status_code=400)
        except DBAPIError:
            return resp(conn_err_msg, content_type='text/plain', status_int=400)
        except:
            print (exc_info())
            return resp(json=dict(rc=400, msg="Login Error: unknown error"), status_code=400)

    #Signup
    @view_config(route_name='signup', request_method='OPTIONS')
    def signup_options(self):
        resp = self.request.response
        return resp

    @view_config(route_name='signup')
    def signup(self):
        request = self.request
        resp = request.response
        user = Userinfo()
        username=request.json_body.get('username')
        email = request.json_body.get('email')
        pwd = request.json_body.get('password')
        salt = bcrypt.gensalt()
        #user.pwhash = bcrypt.hashpw(bytes(request.POST.get('password'), 'utf-8'), user.salt)
        #user.active = False

        #user.key = bcrypt.hashpw(bytes(request.POST.get('email'), 'utf-8'), bcrypt.gensalt())

        from models import AddNewUser
        Uid=AddNewUser(username,pwd,email,salt)
        if Uid>0:
            from Authentication import generateUserKeys,generateToken
            from models import getUserPubkey
            if generateUserKeys(Uid):
                userToken=generateToken(Uid,pwd)

                return Response(json=dict(rc=200, msg="Sign up: Sign up successful"), status_code=200,accessToken=userToken)
        else:
            return Response(json=dict(rc=200, msg="Sign up: Sign up fail"), status_code=200,userToken=None,userPubKey=None)

    # save a posted image

    @view_config(route_name='post', request_method='OPTIONS')
    def post_options(self):
        resp = self.request.response  # (json=dict(rc=200, msg="Options Successful"), status_code=200)
        # resp.headerlist.append(('Access-Control-Allow-Origin', 'http://localhost:8000'))
        return resp

    @view_config(route_name='post', request_method='POST')
    def post(self):
        request = self.request
        resp = request.response
        #TODO: authentication of user request
        #userToken=json.loads(request.POST.get('accessToken'))
        #userid=json.loads(request.POST.get('userid'))
        #if not authenticateUser(userid,userToken):
        #    return
            #TODO: redirect to login page

        # ``filename`` contains the name of the file in string format.
        #
        # WARNING: this example does not deal with the fact that IE sends an
        # absolute file *path* as the filename.  This example is naive; it
        # trusts user input.

        #TODO:change the filename filter
        try:
            filename = request.POST['file'].filename
            tagString=request.POST['tags']
            tags=list()
            if (tagString is not None):
                import json
                try:
                    tags=json.loads(tagString)
                except:
                    tags=list()
            else:
                tags=list()
            # ``input_file`` contains the actual file data which needs to be
            # stored somewhere.
            if (filename):
                input_file = request.POST['file'].file
                # strip leading path from file name to avoid directory traversal attacks
                fn = os.path.basename(filename)
                # open('../static/img/' + fn, 'wb').write(input_file.file.read())

                # Note that we are generating our own filename instead of trusting
                # the incoming filename since that might result in insecure paths.
                # Please note that in a real application you would not use /tmp,
                # and if you write to an untrusted location you will need to do
                # some extra work to prevent symlink attacks.
                #RealPath='/Users/zoe/Desktop/Projects/lc_frontend/app/images/uploaded'
                RealPath = 'C:\\LC\\lc_ng\\app\\images\\uploaded'
                RelativePath = os.path.join('images', 'uploaded')
                Saved_file_name = '%s' % uuid.uuid4() + '.' + fn.rpartition('.')[2]
                file_path = os.path.join(RealPath, Saved_file_name)
                Relative_file_path = os.path.join(RelativePath, Saved_file_name)
                # We first write to a temporary file to prevent incomplete files from
                # being used.

                temp_file_path = file_path + '~'

                # Finally write the data to a temporary file
                input_file.seek(0)
                with open(temp_file_path, 'wb') as output_file:
                    shutil.copyfileobj(input_file, output_file)

                # Now that we know the file has been fully saved to disk move it into place.

                os.rename(temp_file_path, file_path)
                resp.status_code = 200

                userid=json.loads(request.POST.get('userid'))
                #userid=user_object['userid']

                pic_id = postevents.addphotoEvent(userid, RelativePath,Saved_file_name,tags)

                if (pic_id>0):
                    return dict(rc=200, msg="File uploaded")
                else:
                    return dict(rc=400, msg="Error in Upload Picture")
            else:
                resp.status_code = 400
                return dict(rc=400, msg="no file name")
        except:
            print (exc_info())
            resp.status_code = 400
            return dict(rc=400, msg="Post Error: unknown error")

    #Fetch Feeds
    @view_config(route_name='main', request_method='OPTIONS')
    def main_options(self):
        resp = self.request.response
        return resp

    @view_config(route_name='main')
    def main(self):
        request = self.request
        resp = request.response

        userid = request.json_body.get('userid')
        page = request.json_body.get('page')

        result = list()

        result = postevents.loaduserFeeds(userid,page)

        try:
            # fetch feeds by using userid here
            return dict(rc=200, msg="Fetch Feeds Successful", feeds=result)
        except:
            print (exc_info())
            resp.status_code = 400
            return dict(rc=400, msg="Fetch Feeds Error: unknown error")

    # search
    @view_config(route_name='search', request_method='OPTIONS')
    def search_options(self):
        resp = self.request.response
        return resp

    @view_config(route_name='search', request_method='GET')
    def search(self):
        request = self.request
        resp = self.request.response
        keyword = request.params.get('keyword', 'No word Provided')
        if (keyword=='No word Provided'):
            return resp(json=dict(rc=400, msg="No keyword"), status_code=400)
        else:
            from ProductSearch import SearchProductByKeyword
            result=SearchProductByKeyword(keyword)
            #dict(name=product._productName,price=product._price,url=product._webUrl, brand=product._brand)
            return dict(rc=200, msg="result", results=result)

    # Add Comment
    @view_config(route_name='addcomment', request_method='OPTIONS')
    def addcomment_options(self):
        resp = self.request.response
        return resp

    @view_config(route_name='addcomment', request_method='POST')
    def addcomment(self):
        request = self.request
        resp = self.request.response
        try:
            #Add comment to DB
            user_id = request.json_body.get('userid')
            pic_id = request.json_body.get('picid')
            comment = request.json_body.get('comment')

            comms = postevents.adduserComment(user_id, pic_id, comment)
            if (comms is not None):
                return dict(rc=200, msg="Comment Added", comments=comms)
            else:
                return dict(rc=400, msg="Comment Added Failed", comments=None)
        except:
            print (exc_info())
            return resp(json=dict(rc=400, msg="Comment Error: " + exc_info()), status_code=400)

    # Add/Delete Like
    @view_config(route_name='addlike', request_method='OPTIONS')
    def addlike_options(self):
        resp = self.request.response
        return resp

    @view_config(route_name='addlike', request_method='POST')
    def addlike(self):
        request = self.request
        resp = self.request.response
        try:
            from postevents import addUserLikePhoto
            #Add/Delete like to DB

            user_id = request.json_body.get('userid')
            pic_id = request.json_body.get('picid')
            result=addUserLikePhoto(user_id,pic_id)
            if (result is not None):
                return dict(rc=200, msg="likes Added",likeCount=result)
            else:
                return dict(rc=400, msg="Likes Added Failed")

        except:
            print (exc_info())
            return resp(json=dict(rc=400, msg="Comment Error: " + exc_info()), status_code=400)

    #Add Favorite
    @view_config(route_name='addfavorite', request_method='OPTIONS')
    def addfavorite_options(self):
        resp = self.request.response
        return resp

    @view_config(route_name='addfavorite', request_method='POST')
    def addfavorite(self):
        request = self.request
        resp = self.request.response
        try:
            #Add/Delete like to DB
            user_id = request.json_body.get('userid')
            pic_id = request.json_body.get('picid')

            fav = postevents.addPhotoFavorite(user_id, pic_id)

            if(fav):
                return dict(rc=200, msg="Favorite Added")
            else:
                return dict(rc=400, msg="Favorite Added Failed")
        except:
            print (exc_info())
            return resp(json=dict(rc=400, msg="add favorite Error: " + exc_info()), status_code=400)

    # Get User Profile
    @view_config(route_name='userprofile', request_method='OPTIONS')
    def userprofile_options(self):
        resp = self.request.response
        return resp

    @view_config(route_name='userprofile', request_method='GET')
    def userprofile(self):
        request = self.request
        resp = self.request.response

        try:
            userid = request.params.get('userid')

            profile = postevents.getUserProfilePage(userid)

            return dict(rc=200, msg="Get Profile Successful", profile=profile)
        except:
            print (exc_info())
            return dict(rc=400, msg="User Profile Error: " + exc_info(), status_code=400)

    @view_config(route_name='updateprofile', request_method='POST')
    def updateprofile(self):
        request = self.request
        resp = self.request.response

        try:
            userid = request.params.get('userid')

            profile = postevents.getUserProfilePage(userid)

            return dict(rc=200, msg="Update Profile Successful", profile=profile)
        except:
            print (exc_info())
            return dict(rc=400, msg="Update User Profile Error: " + exc_info(), status_code=400)

    # Get User Posts
    @view_config(route_name='userposts', request_method='OPTIONS')
    def userposts_options(self):
        resp = self.request.response
        return resp

    @view_config(route_name='userposts', request_method='GET')
    def userposts(self):
        request = self.request
        resp = self.request.response

        try:
            userid = request.params.get('userid')

        except:
            print (exc_info())
            return resp(json=dict(rc=400, msg="User Post Error: " + exc_info()), status_code=400)

    # Get User Fav
    @view_config(route_name='userfav', request_method='OPTIONS')
    def userfav_options(self):
        resp = self.request.response
        return resp

    @view_config(route_name='userfav', request_method='GET')
    def userfav(self):
        request = self.request
        resp = self.request.response

        try:
            userid = request.params.get('userid')

        except:
            print (exc_info())
            return resp(json=dict(rc=400, msg="User Fav Error: " + exc_info()), status_code=400)

conn_err_msg = """
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
