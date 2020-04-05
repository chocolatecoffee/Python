import os
import socket
import datetime
import ast
import logging
import sys
import xmlrpc.server as rpc


class Rpc_server:

    rpc_paths = ('/RPC2',)

    # ポート番号
    _PORT = 50000

    # 受信バッファの大きさ
    _BUFSIZE = 4096

    # ServerIP
    _SERVER_IP = '192.168.100.2'

    # logfile
    logging.basicConfig(level=logging.DEBUG, filename='./Log_Server.txt', filemode='w',
                        format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

    def Main(self):
        ''''''
        with rpc.SimpleXMLRPCServer((self._SERVER_IP, self._PORT)) as server:

            server.register_introspection_functions()

            def Respons(x):
                return x+'!!!'

            def View(y):
                print(y)
                return ''

            server.register_function(Respons, 'res')
            server.register_function(View, 'view')

            print('Serving XML-RPC on localhost port 50000')
            server.serve_forever()

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
    myclass = Rpc_server()
    myclass.Main()
    del myclass
    logging.debug('AA')
