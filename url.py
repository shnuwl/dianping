import logging
from shop import Shop

if __name__ == '__main__':
    logging.basicConfig(level="DEBUG",
                        filename="D:\dp_more.log",
                        format="%(asctime)s[%(levelname)s][%(filename)s.%(funcName)s]%(message)s")
    Shop().get_all_info()
