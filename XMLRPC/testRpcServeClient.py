import ast
import datetime
import json
import logging
import os
import socket
import sys
import subprocess

import Rpc_client


class testRpcServeClient:

    _jsondata = './TestClientMsg.json'

    # logfile
    logging.basicConfig(level=logging.DEBUG, filename='./TestLog.log', filemode='w',
                        format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

    def _LoadJSON(self):
        '''JSONの読み取り ”_jsondata”を読み取る'''
        logging.debug('VV')

        return json.load(open(self._jsondata, 'r', encoding='UTF-8'))

    def Main(self):
        ''''''
        # JSONファイル取得方法
        client = Rpc_client.Rpc_client()
        jsons = client.RequestJSON()
        setttings = jsons.get('Settings.json')
        applicationitiran_json = jsons.get('ApplicationItiran.json')
        print(type(setttings))
        print(setttings.get('maruMark'))

        pshells = client.RequestPowerShell()
        pshell_getime = pshells.get('GetIMELangSettingList_.ps1')
        pshell_getStore = pshells.get('GetStoreApplication_.ps1')

        with open('./Test.ps1', mode='w', encoding='UTF-8') as f:
            f.write(pshell_getStore)

        subprocess.run('chcp 65001', shell=True)

        proc = subprocess.run('C://Windows//system32//WindowsPowerShell//v1.0//powershell.exe .//Test.ps1', shell=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 取得した一覧をUTF-8に変換 結果が一行で出力されるので改行（\r\n）で区切る
        print(proc.stdout.decode('UTF-8').split('\r\n'))
        # print(proc.stdout)

        # サーバへ結果JSONを戻す方法
        client.SendMsg('savefilename.json', setttings)

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
    myclass = testRpcServeClient()
    myclass.Main()
    del myclass
    logging.debug('AA')
