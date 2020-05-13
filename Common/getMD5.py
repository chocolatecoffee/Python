import logging
import hashlib

# ログレベルのフォーマット Log.txtファイルに出力
logging.basicConfig(level=logging.DEBUG, filename='Log.txt',
                    format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

testFile = "C:\\Windows\\explorer.exe"


class getMD5:
    '''ファイルのMD5を求める。'''

    def checkMd5(self, fileName):
        '''ファイルのMD5を算出するよ'''

        md5 = hashlib.md5()
        with open(fileName, "rb") as f:
            for chunk in iter(lambda: f.read(2048 * md5.block_size), b''):
                md5.update(chunk)
        checksum = md5.hexdigest()
        # print(checksum)
        return checksum

    def main(self):
        logging.debug(' プログラム開始 ')
        print("-----")
        self.checkMd5(testFile)
        logging.debug(' プログラム終了 ')

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


if __name__ == "__main__":
    logging.debug('VV')
    myclass = getMD5()
    myclass.main()

    logging.debug('AA')
