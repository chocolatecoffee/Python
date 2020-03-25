import socket
import datetime
import threading

import json
import logging


class TCPServer:

    # ポート番号
    _PORT = 50000

    # 受信バッファの大きさ
    _BUFSIZE = 4096

    # ServerIP
    _SERVER_IP = '192.168.100.2'

    _jsondata = './Test.json'

    # logfile
    logging.basicConfig(level=logging.DEBUG, filename='./Log.txt', filemode='w',
                        format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

    def _LoadJSON(self):
        '''JSONの読み取り ”_jsondata”を読み取る'''
        logging.debug('VV')

        # Json読み取り
        return json.load(open(self._jsondata, 'r'))

    def Request(self):
        ''''''

    def Main(self):
        ''''''

        #　クライアントの受付番号の初期化
        clientNo = 0

        # ソケットの作成
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

            # アドレスの設定
            server.bind((self._SERVER_IP, self._PORT))

            print(str(datetime.datetime.now()), '  Waiting...')

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

                # クライアントより受信
                data = client.recv(self._BUFSIZE)

                # 受信内容の出力
                print('(', clientNo, ')', data.decode('UTF-8'))

                # メッセージの送信
                client.sendall(b'HI')

                # コネクションのクローズ
                client.close()

    def __init__(self):
        ''''''


if __name__ == '__main__':

    logging.debug('VV')
    myclass = TCPServer
    myclass.Main(myclass)
    logging.debug('AA')
