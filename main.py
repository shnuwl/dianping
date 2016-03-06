import logging
from parse import Parse

if __name__ == '__main__':
    logging.basicConfig(level="DEBUG",
                        filename="/var/log/dp_more.log",
                        format="%(asctime)s[%(levelname)s][%(filename)s.%(funcName)s]%(message)s")
    Parse().parse_all_info()
