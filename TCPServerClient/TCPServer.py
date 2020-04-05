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

    def ExeServer(self):
        '''[summary]'''

        strjson = self._DumpJSON()

        #　クライアントの受付番号の初期化
        clientNo = 0

        # ソケットの作成
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

            # ブロッキング
            server.setblocking(True)
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
                print(str(datetime.datetime.now()),
                      'Connection Request(', clientNo, '):', str(addr))

                # クライアントより受信
                # 受信内容の出力
                print('(', clientNo, ')', client.recv(
                    self._BUFSIZE).decode('utf-8'))

                # メッセージの送信
                client.sendall(strjson)

                # コネクションのクローズ
                client.close()

    def Main(self):
        ''''''

        self.ExeServer()

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
    myclass = TCPServer()
    myclass.Main()
    del myclass
    logging.debug('AA')
