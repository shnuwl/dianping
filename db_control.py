#encoding=utf-8
import logging
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# sys.path.append(os.path.dirname(os.path.realpath(__file__)))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from db_info import DB_Session

Base = declarative_base()
_Logger = logging.getLogger(__name__)

class MysqlControl:
    def __init__(self):
        self.session= DB_Session()

    def add_shop(self, res):
        new_shop = Shop(id=res['shopId'],
                        name=res['basicInfo'][0],
                        level=res['basicInfo'][1],
                        perConsume=res['basicInfo'][2],
                        taste=res['basicInfo'][3],
                        environment=res['basicInfo'][4],
                        service=res['basicInfo'][5],
                        addr=res['basicInfo'][6],
                        phoneNum=res['phoneNum'],
                        cityName=res['cityName'])
        self.session.merge(new_shop)
        self.session.commit()
        print "Added shopId: {0}".format(res['shopId'])

    def add_comment(self, res):
        query = self.session.query(Comment.id)
        scalar = query.filter(Comment.shopId == res['shopId'],
                              Comment.userName == res['userName'],
                              Comment.text == res['text']).scalar()
        if not scalar:
            if not res['rst']:
                res['rst'] = ['-', '-', '-']
            new_comment = Comment(shopId=res['shopId'],
                                  userName= res['userName'],
                                  taste=res['rst'][0],
                                  environment=res['rst'][1],
                                  service=res['rst'][2],
                                  text=res['text'],
                                  time=res['time'])
            self.session.add(new_comment)
            self.session.commit()
            print "Added comment from {0}".format(res['userName'])

class Shop(Base):
    __tablename__ = 'shop'

    id = Column(String(10), primary_key=True)
    name = Column(String(20))
    level = Column(String(8))
    perConsume = Column(String(8))
    taste = Column(String(3))
    environment = Column(String(3))
    service = Column(String(8))
    addr = Column(String(60))
    phoneNum = Column(String(15))
    cityName = Column(String(8))

class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    shopId = Column(String(10))
    userName = Column(String(20))
    taste = Column(String(3))
    environment = Column(String(3))
    service = Column(String(8))
    text = Column(String(500))
    time = Column(String(15))

