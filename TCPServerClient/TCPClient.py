import socket
import datetime
import ast
import logging

class TcpClient:

    # ポート番号
    _PORT = 50000

    # 受信バッファの大きさ
    _BUFSIZE = 4096

    # ServerIP
    _SERVER_IP = '192.168.100.2'

    # logfile
    logging.basicConfig(level=logging.DEBUG, filename='./Log.txt', filemode='w',
                        format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

    def RequestServer(self):
        '''[_SERVER_IPへリクエストする．]
        '''        

        print('The client started at', str(datetime.datetime.now()))

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.connect((self._SERVER_IP, self._PORT))
            server.sendall(b'Hello TCP')
            dictobj = ast.literal_eval(server.recv(self._BUFSIZE).decode())
            print(type(dictobj))
            print(dictobj['TEST_03'])

    def Main(self):
        ''''''
        
        self.RequestServer(self)

    def __init__(self):
        ''''''

if __name__ == '__main__':

    logging.debug('VV')
    myclass = TcpClient
    myclass.Main(myclass)
    logging.debug('AA')
