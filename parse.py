# coding=utf-8
import datetime
import logging
import re

from bs4 import BeautifulSoup
from db_control import MysqlControl
from content import Content

_Logger = logging.getLogger(__name__)

class Parse(object):

    def __init__(self):
        self.content = Content()
        self.db = MysqlControl()
        self._RST_RE = re.compile(r'\d+')
        self._ID_RE0 = re.compile(r'shopId:\s*(\d+)')
        self._ID_RE1 = re.compile(r'shopID:\s*(\d+)')
        self._NAME_RE = re.compile(r'cityCnName:\s*"(\S+)"')
        self._PHONE_RE = re.compile(r'电话：</span>\s+.+tel">(\d{3,4}.\d+)')
        self._REPLY_RE = re.compile(r'J-busi-reply')

    def parse_shop(self, info):
        basicInfo = list()
        soup = BeautifulSoup(info, "html5lib")
        shop_name_tag = soup.find(class_='shop-name')
        shop_brief_tag = soup.find(class_='brief-info')
        shop_addr_tag = soup.find(class_='expand-info address')
        addr = shop_addr_tag.find_all(class_='item')[0].string
        items = shop_brief_tag.find_all(class_='item')
        basicInfo.append(shop_name_tag.contents[0].string.strip())
        basicInfo.append(shop_brief_tag.span['title'])
        for item in items[1:]:
            basicInfo.append(item.string[3:])
        if len(basicInfo) == 3:
            basicInfo.extend(['-']*3)
        basicInfo.append(addr.strip())
        shopId = self._ID_RE0.findall(info)[0]
        cityName = self._NAME_RE.findall(info)[0]
        phone_list = self._PHONE_RE.findall(info)
        if phone_list:
            phoneNum = phone_list[0]
        else:
            phoneNum = '-'
        res = {'shopId': shopId,
               'cityName': cityName,
               'phoneNum': phoneNum,
               'basicInfo': basicInfo
        }
        self.db.add_shop(res)
        _Logger.info('shop {0}\'s basic info has saved'.format(shopId))

    def parse_comment(self, comment):
        shopId = self._ID_RE1.findall(comment)[0]
        soup = BeautifulSoup(comment, "html5lib")
        div_tag = soup.find(class_='comment-list')
        content_tag = div_tag.find_all(class_='content')
        user_name_tag = div_tag.find_all(class_='name')
        def func(x, y):
            x.append(y)
            return x

        contents = map(func, content_tag, user_name_tag)
        for content in contents:
            reply_tag = content.find_all('div', self._REPLY_RE)
            time_tag = content.find_all(class_='time')
            text = content.find_all(class_='J_brief-cont')[0].contents[0].strip()
            if reply_tag:
                text += '\n' + reply_tag[0].find_all('p')[0].text.strip()
            userName = content.find(class_='name').contents[0].string
            rst = []
            for x in content.find_all(class_='rst'):
                rst.extend(self._RST_RE.findall(x.contents[0]))
            time = time_tag[0].contents[0]
            if len(time) == 5:
                year = datetime.datetime.now().strftime('%y')
                time = year + '-' + time
            res = {'shopId': shopId,
                   'userName': userName,
                   'rst': rst,
                   'text': text,
                   'time': time
            }
            self.db.add_comment(res)
        _Logger.info('shop {0}\'s comments info has saved'.format(shopId))

    def parse_all_info(self):
        for info, comment in self.content.get_all_contents():
            self.parse_shop(info)
            self.parse_comment(comment)
