# -*- coding: utf-8 -*-
import logging
import time

from multiprocessing import Pool,Process,TimeoutError
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor


# logfile
logging.basicConfig(level=logging.DEBUG, filename='./Log.txt', filemode='w',
                    format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

class MultiProcessAndThread:

    def killing_time(self,number):
        print(number)
        return_list = []
        for i in range(1, number + 1):
            if number % i == 1:
                if i <= 9999:
                    return_list.append(i)

    def RequestOrders(self, order):
        print('{}うどんを作ります。\n'.format(order))
        time.sleep(1)
        print('{}うどんあがりました。\n'.format(order))

    def ViewTime(self,start,stop):
        print('%.3f seconds \n' % (stop - start))

    def MultiProcessingPool(self,order,lst):
        print('MultiProcessingPool:')
        start = time.time()

        with Pool(processes=4) as pool:
            pool.map(self.RequestOrders,order)
            pool.map(self.killing_time,lst)

        stop = time.time()
        self.ViewTime(start,stop)
        
    def ProcessPool(self,order,lst):
        print('ProcessPool:')
        start = time.time()

        with ProcessPoolExecutor(max_workers=4) as executor:
            executor.map(self.RequestOrders, order)
            executor.map(self.killing_time, lst)

        stop = time.time()
        self.ViewTime(start,stop)



    def ThreadPool(self,order,lst):
        print('MultiThread:')
        start = time.time()

        with ThreadPoolExecutor(max_workers=4, thread_name_prefix="thread") as executor:
            
            for _ in order:
                executor.submit(self.RequestOrders, _)
                executor.shutdown
            
            for _ in lst:
                executor.submit(self.killing_time, _)
                executor.shutdown

        stop = time.time()
        self.ViewTime(start,stop)

    def Main(self):
        orders = ['わかめ', 'コロッケ', 'カレー', '山菜','おあげ', '天ぷら', '牛すき', '鴨', 'そば', '具なし']
        num_list = [25000000, 20000000, 20076000, 14500000,25000000, 20000000, 20076000, 14500000]

        self.MultiProcessingPool(orders,num_list)
        self.ProcessPool(orders,num_list)

        self.ThreadPool(orders,num_list)

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
    myclass = MultiProcessAndThread()
    myclass.Main()
    del myclass
    logging.debug('AA')