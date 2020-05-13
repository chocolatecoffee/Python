import os
import socket
import datetime
import ast
import json
import logging
import sys
import xmlrpc.server as rpc


class Rpc_server:

    # ポート番号
    _PORT = 50000

    # 受信バッファの大きさ
    _BUFSIZE = 4096

    # ServerIP
    _SERVER_IP = '192.168.100.2'

    # Rpc_clientに渡すJSON
    _json_ApplicationItiran = './ApplicationItiran.json'
    _json_Settings = './Settings.json'

    # logfile
    logging.basicConfig(level=logging.DEBUG, filename='./Log_Server.txt', filemode='w',
                        format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

    def StartServer(self):
        '''[summary]

        Returns:
            [type]: [description]
        '''

        with rpc.SimpleXMLRPCServer((self._SERVER_IP, self._PORT), requestHandler=rpc.SimpleXMLRPCRequestHandler) as server:

            server.register_introspection_functions()

            def GetJSON():
                '''JSONの読み取り ”_jsondata”を読み取る'''

                json_Stngs = None
                json_App = None

                try:
                    logging.debug('VV')
                    json_App = json.load(
                        open(self._json_ApplicationItiran, 'r', encoding='UTF-8'))
                    json_Stngs = json.load(
                        open(self._json_Settings, 'r', encoding='UTF-8'))
                except FileNotFoundError as exp:
                    logging.exception(exp)

                return json_Stngs, json_App

            def SaveMsg(savefilename, msg):
                '''[summary]

                Args:
                    msg ([type]): [description]

                Returns:
                    [type]: [description]
                '''
                return_msg = 'サーバメッセージ:Success!!'

                try:
                    json.dump(msg, open('.//' + savefilename, 'w',
                                        encoding='UTF-8'), ensure_ascii=False, indent=4)
                except Exception as exp:
                    logging.exception(exp)
                    return_msg = 'サーバメッセージ:保存失敗'

                return return_msg

            server.register_function(GetJSON, 'getjson')
            server.register_function(SaveMsg, 'savemsg')

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
        # logging.debug('__del__')


if __name__ == '__main__':

    logging.debug('VV')
    myclass = Rpc_server()
    myclass.Main()
    del myclass
    logging.debug('AA')
