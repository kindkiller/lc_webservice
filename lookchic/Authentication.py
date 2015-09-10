__author__ = 'zoe'

import jwt, Crypto.PublicKey.RSA as RSA, datetime
from models import getUserPubkey,getUserPasswordByID, saveUserKeys,getUserPrivatekey,getUserToken, updateUserToken

def generateToken(userid, userPassword):
    priv_pem=getUserPrivatekey(userid)
    if priv_pem is None:
        print "Error in get user private pem."
        return None
    payload = { 'userid': userid, 'password': userPassword }
    priv_key = RSA.importKey(priv_pem)
    if priv_key is None:
        print "Error in generate user private key."
        return None
    token = jwt.generate_jwt(payload, priv_key, 'RS256', datetime.timedelta(minutes=5))
    if updateUserToken(userid,token):
        return token
    else:
        print "Error in store user token."
        return None


def authenticateUser(userid, token):
    if userid<0:
        return False
    DBToken=getUserToken(userid)
    if DBToken is None:
        return False
    else:
        if token==DBToken:
            return True
        else:
            return False

def authenticateUserPWD(userid, token):
    '''
    Authenticate user with user's userid and password. Not used right now
    :param userid:
    :param token:
    :return: Boolean
    '''
    pub_pem=getUserPubkey(userid)
    if pub_pem is None:
        print "Error in get user public_pem"
        return False
    pub_key=RSA.importKey(pub_pem)
    if pub_key is not None:
        header, claims=jwt.verify_jwt(token,pub_key,['RS256'])
        if claims['userid'] is not None:
            password=claims['password']
            if password==getUserPasswordByID(userid):
                return True
            else:
                return False
        else:
            return False
    else:
        print "Error in generate user public key"
        return False

def generateUserKeys(userID):
    key=RSA.generate(1024)
    priv_pem = key.exportKey()
    pub_pem = key.publickey().exportKey()
    if saveUserKeys(userID,priv_pem,pub_pem):
        return True
    else:
        return False

def refreshUserToken(userID, oldToken):
    if userID <0 or oldToken is None or oldToken=="":
        return None
    newToken=generateToken(userID,getUserPasswordByID(userID))
    if newToken is not None:
        return newToken
    else:
        return None

