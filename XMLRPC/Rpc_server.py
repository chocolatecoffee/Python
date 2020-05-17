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

    _stngs = {}
    '''読みだされた設定情報（Settings.json）を保管用'''

    # Rpc_clientに渡すJSON
    _json_ApplicationItiran = './ApplicationItiran.json'
    _json_Settings = './Settings.json'

    # Rpc_clientに渡すPowerShell
    _pshell_GetIMELangSettingList = './GetIMELangSettingList.ps1'
    _pshell_GetStoreApplication = './GetStoreApplication.ps1'

    # logfile
    logging.basicConfig(level=logging.DEBUG, filename='./Log_Server.txt', filemode='w',
                        format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

    def _LoadJSON(self):
        '''”_json_Settings”を読み取る'''
        logging.debug('VV')

        self._stngs = json.load(
            open(self._json_Settings, 'r', encoding='UTF-8'))

        logging.debug('AA')

    def StartServer(self):
        '''[summary]

        Returns:
            [type]: [description]
        '''

        server = rpc.SimpleXMLRPCServer(
            (self._SERVER_IP, self._PORT), requestHandler=rpc.SimpleXMLRPCRequestHandler)

        server.register_introspection_functions()

        def GetJSON():
            '''[summary]

            Returns:
                [type]: [description]
            '''
            json_Stngs = None
            json_App = None

            try:
                logging.debug('VV')
                json_Stngs = json.load(
                    open(self._json_Settings, 'r', encoding=self._stngs['charcode_01']))
                json_App = json.load(
                    open(self._json_ApplicationItiran, 'r', encoding=self._stngs['charcode_01']))

            except FileNotFoundError as exp:
                logging.exception(exp)

            return {self._stngs['settingfile_01']: json_Stngs, self._stngs['settingfile_02']: json_App}

        def GetPShell():
            '''[summary]

            Returns:
                [type]: [description]
            '''
            send_pshell_getime = None
            send_pshell_getStore = None

            try:
                logging.debug('VV')

                send_pshell_getime = open(
                    self._pshell_GetIMELangSettingList, 'r', encoding=self._stngs['charcode_01']).read()

                send_pshell_getStore = open(
                    self._pshell_GetStoreApplication, 'r', encoding=self._stngs['charcode_01']).read()

            except FileNotFoundError as exp:
                logging.exception(exp)

            return {self._stngs['ps_cmd_01']: send_pshell_getime, self._stngs['ps_cmd_02']: send_pshell_getStore}

        def SaveMsg(savefilename, msg):
            '''[summary]

            Args:
                msg ([type]): [description]

            Returns:
                [type]: [description]
            '''
            return_msg = 'サーバメッセージ:Success!!'

            try:
                json.dump(msg, open('./' + savefilename, 'w',
                                    encoding=self._stngs['charcode_01']), ensure_ascii=False, indent=4)
            except Exception as exp:
                logging.exception(exp)
                return_msg = 'サーバメッセージ:保存失敗'

            return return_msg

        server.register_function(GetJSON, 'getjson')
        server.register_function(GetPShell, 'getpshell')
        server.register_function(SaveMsg, 'savemsg')

        print('Serving XML-RPC on ' + self._SERVER_IP + ':port 50000')
        server.serve_forever()

    def Main(self):
        '''[summary]
        '''
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
        self._LoadJSON()
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
