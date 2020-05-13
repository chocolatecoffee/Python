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

        json_Stngs = None
        json_App = None

        try:
            srv = client.ServerProxy(
                'http://' + self._SERVER_IP + ':' + self._PORT)
            json_Stngs, json_App = srv.getjson()

            if json_Stngs is not None and json_App is not None:
                print("セッティングファイル取得成功")

            else:
                print("セッティングファイル取得失敗")

        except Exception as exp:
            logging.exception(exp)

        return json_Stngs, json_App

    def SendMsg(self, savefilename, msg):
        '''[summary]

        Args:
            msg ([type]): [description]
        '''

        logging.debug('VV')

        srv = client.ServerProxy(
            'http://' + self._SERVER_IP + ':' + self._PORT)
        logging.debug(type(msg))
        print(srv.savemsg(savefilename, msg))

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
