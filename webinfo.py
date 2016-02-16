import logging
import re
import time
import urllib2

_Logger = logging.getLogger(__name__)
_ID_RE = re.compile(r'/shop/(\d+)')

def open_url(url):
    _Logger.info('open_url: {0}'.format(url))
    time.sleep(7)
    # proxy = 'http://122.72.2.180:8080'
    # opener = urllib2.build_opener(urllib2.ProxyHandler({'http':proxy}), urllib2.HTTPHandler(debuglevel=1))
    # urllib2.install_opener(opener)
    i_headers = {'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3',
                 'User-Agent' :  'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US)'
                                  'AppleWebKit/534.16 (KHTML, like Gecko)'
                                  'Chrome/10.0.648.151 Safari/534.16'}
    req = urllib2.Request(url, headers=i_headers)
    return urllib2.urlopen(req).read()

def get_shop_ids(url):
    content = open_url(url)
    return _ID_RE.findall(content)
