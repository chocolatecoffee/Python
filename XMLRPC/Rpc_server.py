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

    _setttings = {}
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
        '''JSONの読み取り ”_jsondata”を読み取る'''
        logging.debug('VV')

        self._setttings = json.load(
            open(self._json_Settings, 'r', encoding='UTF-8'))

        logging.debug('AA')

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
                    json_Stngs = json.load(
                        open(self._json_Settings, 'r', encoding='UTF-8'))
                    json_App = json.load(
                        open(self._json_ApplicationItiran, 'r', encoding='UTF-8'))

                except FileNotFoundError as exp:
                    logging.exception(exp)

                return {self._setttings['settingfile_01']: json_Stngs, self._setttings['settingfile_02']: json_App}

            def GetPShell():
                '''[summary]
                '''

                send_pshell_getime = None
                send_pshell_getStore = None

                try:
                    logging.debug('VV')

                    with open(self._pshell_GetIMELangSettingList, 'r', encoding='UTF-8') as pshell_getime:
                        send_pshell_getime = pshell_getime.read()

                    with open(self._pshell_GetStoreApplication, 'r', encoding='UTF-8') as pshell_getStore:
                        send_pshell_getStore = pshell_getStore.read()

                except FileNotFoundError as exp:
                    logging.exception(exp)

                return {self._setttings['ps_cmd_01']: send_pshell_getime, self._setttings['ps_cmd_02']: send_pshell_getStore}

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
            server.register_function(GetPShell, 'getpshell')
            server.register_function(SaveMsg, 'savemsg')

            print('Serving XML-RPC on ' + self._SERVER_IP + ':port 50000')
            server.serve_forever()

    def Main(self):
        ''''''
        self._LoadJSON()
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
