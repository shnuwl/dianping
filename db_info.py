import web
from configobj import ConfigObj

conf = ConfigObj('config.ini')
db_info = conf['DB']
db_tpms = web.database(dbn='mysql', db = 'dianping', user = db_info['USER'], pw= db_info['PASS'], host = db_info['HOST'])
db_tpms.printing = False
