import os
import socket
import datetime
import ast
import logging
import sys
import xmlrpc.client as client


class rpc_client:

    # ポート番号
    _PORT = 50000

    # 受信バッファの大きさ
    _BUFSIZE = 4096

    # ServerIP
    _SERVER_IP = '192.168.100.2'

    # logfile
    logging.basicConfig(level=logging.DEBUG, filename='./Log_Client.txt', filemode='w',
                        format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

    def Request(self):
        srv = client.ServerProxy('http://192.168.100.2:50000')

        # print(srv.system.listMethods())

        srv.view('This is Me')

        print(srv.res('Respons'))

    def Main(self):
        ''''''
        self.Request()

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
    myclass = rpc_client()
    myclass.Main()
    del myclass
    logging.debug('AA')
