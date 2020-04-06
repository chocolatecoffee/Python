import os
import socket
import datetime
import ast
import json
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

    _jsondata = './Test.json'

    # logfile
    logging.basicConfig(level=logging.DEBUG, filename='./Log_Server.txt', filemode='w',
                        format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

    def _LoadJSON(self):
        '''JSONの読み取り ”_jsondata”を読み取る'''
        logging.debug('VV')

        # Json読み取り
        return json.load(open(self._jsondata, 'r'))

    def _DumpJSON(self):
        '''[_LoadJSONで読み込んだ_jsondataをbyte文字列（utf-8）で返す]

        Returns:
            [byte]: [_jsondataをbyte文字列（utf-8）で返す]
        '''
        logging.debug('VV')

        return json.dumps(self._LoadJSON()).encode('utf-8')

    def StartServer(self):
        '''[summary]

        Returns:
            [type]: [description]
        '''

        strjson = self._DumpJSON()

        with rpc.SimpleXMLRPCServer((self._SERVER_IP, self._PORT)) as server:

            server.register_introspection_functions()

            def GetJSON():

                return strjson

            def SendMsg(msg):
                print(msg)
                return ''

            server.register_function(GetJSON, 'getjson')
            server.register_function(SendMsg, 'sendmsg')

            print('Serving XML-RPC on localhost port 50000')
            server.serve_forever()

    def Main(self):
        ''''''
        self.StartServer()

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
