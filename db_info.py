from configobj import ConfigObj
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

conf = ConfigObj('config.ini')
db_info = conf['DB']
host, user, pwd, db_name = db_info['HOST'], db_info['USER'], db_info['PASS'], db_info['DB_NAME']
DB_CONNECT_STRING = 'mysql+mysqldb://{0}:{1}@{2}:3306/{3}?charset=utf8'.format(user, pwd, host, db_name)
engine = create_engine(DB_CONNECT_STRING, echo=True)
DB_Session = sessionmaker(bind=engine)
