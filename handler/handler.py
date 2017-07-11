import json
import os
import binascii
import tornado.web

from sqlalchemy import create_engine
from sqlalchemy import Column,text, Integer, String, DateTime, Boolean
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy.orm.exc import NoResultFound

from Tools.Tools import *


class BaseHandler(tornado.web.RequestHandler):

    __TOKEN_LIST = {}

    @property
    def db(self):
        return self.application.db


    def generate_token(self):
        while True:
            new_token = binascii.hexlify(os.urandom(16)).decode("utf-8")
            if new_token not in self.__TOKEN_LIST:
                return new_token

    def set_token(self,token,userid):
        self.__TOKEN_LIST[token] = userid
        #self.set_secure_cookie('_token', token)
        

    def get_current_user(self):
        #token = self.get_secure_cookie("_token").decode()
        token = self.get_argument("token",None)
        if token and token in self.__TOKEN_LIST:
            userid = self.__TOKEN_LIST[token]
            return userid
        return None
    
    def valid_user(self):
        token = self.get_argument("token",None)
        user_id = self.get_argument("user_id",None)
        if token and user_id and token in self.__TOKEN_LIST:
            if user_id == self.__TOKEN_LIST[token]:
                return True
        return False
            




#返回附近的歌曲信息
class SongNearHandler(tornado.web.RequestHandler):
    def get(self):
        latitude = self.get_argument("latitude")
        longitude = self.get_argument("longtitude")

        result = []
        rows = getsonginfo()
        for row in rows:
            if(10 > math.fabs(calculateLineDistance(location(longitude, latitude), location(row["longitude"], row["latitude"])))):
                result.append(row)
        self.finish(json.dump(result))







