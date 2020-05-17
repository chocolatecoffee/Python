import os
import socket
import datetime
import ast
import logging
import sys
import xmlrpc.client as client
import json


class rpc_client:

    # ポート番号
    _PORT = '50000'

    # 受信バッファの大きさ
    _BUFSIZE = 4096

    # ServerIP
    _SERVER_IP = '192.168.100.2'

    # logfile
    logging.basicConfig(level=logging.DEBUG, filename='./Log_Client.txt', filemode='w',
                        format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

    def RequestJSON(self):
        '''[summary]

        Returns:
            [type]: [description]
        '''

        logging.debug('VV')

        try:
            return client.ServerProxy(
                'http://' + self._SERVER_IP + ':' + self._PORT).getjson()

        except Exception as exp:
            logging.exception(exp)

    def RequestPowerShell(self):
        '''[summary]

        Returns:
            [type]: [description]
        '''

        logging.debug('VV')

        try:
            return client.ServerProxy(
                'http://' + self._SERVER_IP + ':' + self._PORT).getpshell()

        except Exception as exp:
            logging.exception(exp)

    def SendMsg(self, savefilename, msg):
        '''[summary]

        Args:
            msg ([type]): [description]
        '''

        logging.debug('VV')

        print(client.ServerProxy(
            'http://' + self._SERVER_IP + ':' + self._PORT).savemsg(savefilename, msg))

        logging.debug('AA')

    def Main(self):
        ''''''

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
