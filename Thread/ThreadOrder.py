# -*- coding: utf-8 -*-
import logging
import time

import concurrent.futures as confu

# logfile
logging.basicConfig(level=logging.DEBUG, filename='./Log.txt', filemode='w',
                    format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')


class ThreadOrder:

    def RequestOrders(self, orders):
        with confu.ThreadPoolExecutor(max_workers=3, thread_name_prefix="thread") as executor:
            # executor.map(self.boil_udon, range(10))
            for order in orders:
                executor.submit(self.Order, self, order)

        executor.shutdown

    def Order(self, order):
        print('{}うどんを作ります。\n'.format(order))
        time.sleep(3)
        print('{}うどんあがりました。\n'.format(order))

    def Main(self):
        orders = {'わかめ', 'コロッケ', 'カレー', '山菜',
                  'おあげ', '天ぷら', '牛すき', '鴨', 'そば', '具なし'}

        self.RequestOrders(self, orders)

    def __init__(self):
        ''''''


if __name__ == '__main__':

    logging.debug('VV')
    myclass = ThreadOrder
    myclass.Main(myclass)
    logging.debug('AA')
