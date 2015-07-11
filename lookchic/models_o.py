from pyramid.security import (
    Allow,
    Everyone,
    )

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Sequence,
    String,
    Boolean,
    DateTime,
    Date,
    Table,
    ForeignKey,
    Binary,
    Enum
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )
from sqlalchemy import create_engine

db_uri = "mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db}"
engine = create_engine(db_uri.format(user='allen',password='yao0702',host='192.168.1.103',port='3306',db='userdb'),connect_args={'time_zone':'+00:00'})


from zope.sqlalchemy import ZopeTransactionExtension

#DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

Base = declarative_base()
myDBsession = sessionmaker(bind=engine)
DBSession = myDBsession()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Sequence('user_id_seq', optional=True), primary_key=True)
    # User login entity
    email = Column(String(255), unique=True, nullable=False)
    pwd = Column(String(255))
    #pwhash = Column(Binary(60))

class Page(Base):
    """ The SQLAlchemy declarative model class for a Page object. """
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    data = Column(Text)

class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'view'),
                (Allow, 'group:editors', 'edit') ]
    def __init__(self, request):
        pass
        
