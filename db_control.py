#encoding=utf-8
import logging
import sys
import web
reload(sys)
sys.setdefaultencoding('utf-8')
# sys.path.append(os.path.dirname(os.path.realpath(__file__)))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from db_info import db_tpms

_Logger = logging.getLogger(__name__)

class MysqlControl:
    def __init__(self):
        self.db = db_tpms

    def insert_shop_info(self, res):
        shop_info = list(self.db.select('shop_info',what="shopId",where="shopId=\""+res['shopId']+"\""))
        if shop_info:
            self.db.update('shop_info',
                            where="shopId=\""+res['shopId']+"\"",
                            cityName=res['cityName'],
                            shopName=res['basicInfo'][0],
                            shopLevel=res['basicInfo'][1],
                            perConsume=res['basicInfo'][2],
                            taste=res['basicInfo'][3],
                            environment=res['basicInfo'][4],
                            service=res['basicInfo'][5],
                            addr=res['basicInfo'][6],
                            phoneNum=res['phoneNum']
            )
            print "Added shopId: {0}".format(res['shopId'])
        else:
            self.db.insert('shop_info',
                            shopId=res['shopId'],
                            cityName=res['cityName'],
                            shopName=res['basicInfo'][0],
                            shopLevel=res['basicInfo'][1],
                            perConsume=res['basicInfo'][2],
                            taste=res['basicInfo'][3],
                            environment=res['basicInfo'][4],
                            service=res['basicInfo'][5],
                            addr=res['basicInfo'][6],
                            phoneNum=res['phoneNum']

            )
            print "Added shopId: {0}".format(res['shopId'])

    def insert_shop_comment(self, res):
        where_dict = {'shopId': res['shopId'],
                      'userName': res['userName'],
                      'text':res['text']}
        comment = list(self.db.select('shop_comment',what="shopId",where=web.db.sqlwhere(where_dict)))
        if not comment:
            if not res['rst']:
                res['rst'] = ['-', '-', '-']
            self.db.insert('shop_comment',
                            shopId=res['shopId'],
                            cityName=res['cityName'],
                            shopName=res['shopName'],
                            userName= res['userName'],
                            taste=res['rst'][0],
                            environment=res['rst'][1],
                            service=res['rst'][2],
                            text=res['text'],
                            time=res['time']
            )
            print "Added comment from {0}".format(res['userName'])
