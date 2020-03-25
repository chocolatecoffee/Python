# -*- coding: utf-8 -*-
'''
「PythonによるTCP/IPソケットプログラミング」
https://www.ohmsha.co.jp/book/9784274223242/
server3.pyプログラム
Pythonによるサーバソケットの利用法を示す例題プログラム(3)
50000番ポートで接続を待ち受けてます
クライアントからの入力後、時刻を返します
接続時にコンソールにメッセージを出力します
スレッドを用いて並行処理を行います
Ctrl+Breakで終了します
使いかた　>> python server3.py
'''

# モジュールのインポート
import socket
import datetime
import threading

import json
import logging
import time
import threading

import concurrent.futures as confu


class UdpServer:

    # ポート番号
    _PORT = 50000

    # 受信バッファの大きさ
    _BUFSIZE = 4096

    # ServerIP
    _SERVER_IP = '192.168.100.2'

    _jsondata = ''

    # logfile
    logging.basicConfig(level=logging.DEBUG, filename='./Log.txt', filemode='w',
                        format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

    def _LoadJSON(self):
        '''JSONの読み取り ”_jsondata”を読み取る'''
        logging.debug('VV')

        # Json読み取り
        return json.load(open(self._jsondata, 'r'))

    def ClientHandler(self, client, clientno, msg):
        '''クライアントとの接続処理スレッド'''

        # クライアントより受信
        data = client.recv(self._BUFSIZE)
        # data, client_ip = client.recvfrom(self._BUFSIZE)

        # 受信内容の出力
        print('(', clientno, ')', data.decode('UTF-8'))

        # メッセージの送信
        client.sendall(msg.encode('UTF-8'))

        # コネクションのクローズ
        client.close()

    def Order(self, order):
        print('{}うどんを作ります。うどんを茹でます。\n'.format(order))
        time.sleep(3)
        print('あがりました。\n')

    def RequestOrders(self, orders):
        with confu.ThreadPoolExecutor(max_workers=4, thread_name_prefix="thread") as executor:
            # executor.map(self.boil_udon, range(10))
            for order in orders:
                executor.submit(self.Order, self, order)

        executor.shutdown

    def Main(self):

        orders = {'わかめ', 'コロッケ', 'カレー', '山菜',
                  'おあげ', '天ぷら', '牛すき', '鴨', 'そば', '具なし'}

        self.RequestOrders(self, orders)

        #　クライアントの受付番号の初期化
        clientNo = 0

        # ソケットの作成
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

                # アドレスの設定
            server.bind((self._SERVER_IP, self._PORT))

            # 接続の待ち受け
            server.listen()

            # クライアントへの対応処理
            while True:
                # 通信用ソケットの取得
                client, addr = server.accept()

                # 受付番号のカウントアップ
                clientNo += 1

                # メッセージの作成
                msg = str(datetime.datetime.now())

                print(msg, 'Connection Request(', clientNo, '):', client)

                # スレッドの設定と起動
                threading.Thread(target=self.ClientHandler, args=(
                    self, client, clientNo, msg)).start()

    def __init__(self):
        ''''''


if __name__ == '__main__':

    logging.debug('VV')
    myclass = UdpServer
    myclass.Main(myclass)
    logging.debug('AA')
