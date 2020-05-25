import logging
import csv

import sys

# ログレベルのフォーマット Log.txtファイルに出力
logging.basicConfig(level=logging.DEBUG, filename='Log.txt', filemode='w',
                    format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')


class CsvLoader:
    '''[CSV・・・ character separated valuesのことなのでTabでもスペースでもChara扱いなのです。]
    '''

    def LoadCSV_Dict(self, csvfile):
        '''[summary]

        Args:
            csvfile ([type]): [description]

        Returns:
            [type]: [description]
        '''

        logging.debug('VV')
        reader = None
        _ = []

        try:
            with open(csvfile, encoding='UTF-8', newline='') as f:
                reader = csv.DictReader(f, delimiter=':')

                for row in reader:
                    _.append(row)

        except Exception as e:
            sys.exit('file {}, line {}: {}'.format(
                csvfile, reader.line_num, e))

        logging.debug('AA')
        return _

    def LoadCSV(self, csvfile):
        '''[summary]

        Args:
            csvfile ([type]): [description]

        Returns:
            [type]: [description]
        '''

        logging.debug('VV')
        reader = None
        _ = []

        try:
            with open(csvfile, encoding='UTF-8', newline='') as f:
                reader = csv.reader(f, delimiter=':')

                for row in reader:
                    _.append(row)

        except Exception as e:
            sys.exit('file {}, line {}: {}'.format(
                csvfile, reader.line_num, e))

        logging.debug('AA')
        return _

    def LoadTSV_Dict(self, csvfile):
        '''[summary]

        Args:
            csvfile ([type]): [description]

        Returns:
            [type]: [description]
        '''

        logging.debug('VV')
        reader = None
        _ = []

        try:
            with open(csvfile, encoding='UTF-8', newline='') as f:
                reader = csv.DictReader(f, delimiter='\t')

                for row in reader:
                    _.append(row)

        except Exception as e:
            sys.exit('file {}, line {}: {}'.format(
                csvfile, reader.line_num, e))

        logging.debug('AA')
        return _

    def LoadTSV(self, csvfile):
        '''[summary]

        Args:
            csvfile ([type]): [description]

        Returns:
            [type]: [description]
        '''

        logging.debug('VV')
        reader = None
        _ = []

        try:
            with open(csvfile, encoding='UTF-8', newline='') as f:
                reader = csv.reader(f, delimiter='\t')

                for row in reader:
                    _.append(row)

        except Exception as e:
            sys.exit('file {}, line {}: {}'.format(
                csvfile, reader.line_num, e))

        logging.debug('AA')
        return _

    def Main(self):
        logging.debug('VV')
        logging.debug('AA')

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
    myclass = CsvLoader()
    myclass.Main()
    logging.debug('AA')
