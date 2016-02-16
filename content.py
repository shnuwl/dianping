import logging

from configobj import ConfigObj
from webinfo import open_url, get_shop_ids

CONF = ConfigObj('config.ini')
PAGE = CONF['PAGE']
NUM = PAGE['NUM']

_Logger = logging.getLogger(__name__)

class Content(object):

    def __init__(self):
        self.init_url = 'http://wap.dianping.com/shoplist/1/r/0/c/10/s/s_3/p'
        self._URL_PRE = 'http://www.dianping.com/shop/'
        self._COMMENT_SUF = '/review_all'

    def _get_shop_comment_urls(self):
        for i in xrange(int(NUM), 6000):
            shop_ids = get_shop_ids(self.init_url + str(i))
            _Logger.info('the number: {0}'.format(str(i)))
            for _id in shop_ids:
                shop_url = self._URL_PRE + _id
                comment_url = shop_url + self._COMMENT_SUF
                _Logger.info('shop_url: {0}'.format(shop_url))
                _Logger.info('comment_url: {0}'.format(comment_url))
                yield shop_url, comment_url

    def get_all_contents(self):
        for shop_url, comment_url in self._get_shop_comment_urls():
            yield open_url(shop_url), open_url(comment_url)

