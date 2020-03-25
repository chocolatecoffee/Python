# -*- coding: utf-8 -*-
'''
「PythonによるTCP/IPソケットプログラミング」
https://www.ohmsha.co.jp/book/9784274223242/
client1.pyプログラム
Pythonによるクライアントソケットの利用法を示す例題プログラム(1)
50000番ポートで、指定したサーバに接続します
接続後、サーバにメッセージを送ります
その後、サーバからのメッセージを取得して表示します
使いかた >> python client1.py
'''

# モジュールのインポート
import socket
import sys

import json
import logging


class UdpClient:

    _SERVER_IP = '192.168.100.2'

    # ポート番号
    _PORT = 50000

    # 受信バッファの大きさ
    _BUFSIZE = 4096

    _jsondata = ''

    # logfile
    logging.basicConfig(level=logging.DEBUG, filename='./Log.txt', filemode='w',
                        format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

    def Main(self):

        # ソケットの作成
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:

            #host = input('接続先サーバ：')

            try:
                client.connect((self._SERVER_IP, self._PORT))
            except:
                print('接続できません')
                sys.exit()

            # サーバへのメッセージの送信
            #msg = input('メッセージを入力：')
            sendmsg = 'This is Me'
            client.sendall(sendmsg.encode('UTF-8'))

            # サーバからのメッセージの受信
            receivedmsg = client.recv(self._BUFSIZE)
            print('サーバからのメッセージ：{}'.format(receivedmsg.decode('UTF-8')))


def __init__(self):
    ''''''


if __name__ == '__main__':
    # ダブルクリックなどで実行された場合に”__name__”に”__name__”と入るのでここが実行される
    logging.debug('VV')
    myclass = UdpClient
    myclass.Main(myclass)
    logging.debug('AA')
