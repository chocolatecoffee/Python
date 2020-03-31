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
                executor.submit(self.Order, order)

        executor.shutdown

    def Order(self, order):
        print('{}うどんを作ります。\n'.format(order))
        time.sleep(3)
        print('{}うどんあがりました。\n'.format(order))

    def Main(self):
        orders = {'わかめ', 'コロッケ', 'カレー', '山菜',
                  'おあげ', '天ぷら', '牛すき', '鴨', 'そば', '具なし'}

        self.RequestOrders(orders)

    def __new__(cls):
        '''[summary]

        Returns:
            [type]: [description]
        '''

        logging.debug('__new__')
        self = super().__new__(cls)
        return self

    def __init__(self):
        '''[summary]
        '''

        logging.debug('__init__')

    def __del__(self):
        '''[summary]
        '''
        logging.debug('__del__')


if __name__ == '__main__':

    logging.debug('VV')
    myclass = ThreadOrder()
    myclass.Main()
    del myclass
    logging.debug('AA')
