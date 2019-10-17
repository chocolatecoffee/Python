import logging
import json
import datetime
from collections import OrderedDict
import os

# ログレベルのフォーマット Log.txtファイルに出力
logging.basicConfig(level=logging.DEBUG, filename='.\\Log.txt',
                    format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s', filemode='w')


class LoadAndAddJSON:

    '''[summary]

    Returns:
        [type]: [description]
    '''

    _today = datetime.datetime.now()
    # datetime obj

    # _today = datetime.datetime.now().isoformat()
    # today 2019-10-17T23:11:56.338690

    _jsonfile = '.\\{}_TEST.json'.format(_today.year)

    # 新規作成用のJSON
    _Newjson_format = {}

    def load_JSON(self, jsonfile):
        '''[summary]
            Returns:
            [type]: [description]
        '''
        logging.debug('VV')

        if (os.path.exists(jsonfile)):
            logging.debug(jsonfile)

        else:

            # with open(jsonfile, 'w') as f:
            #    f.write("")
            logging.debug(jsonfile)
            json.dump(self._Newjson_format, open(
                jsonfile, 'w'), indent=4)

        logging.debug('AA')

        return json.load(open(jsonfile, 'r'))

    def add_JSON(self, jsonobj):
        '''[summary]

        Args:
            json ([type]): [description]
        '''
        logging.debug('VV')

        # print(today.year, "年", today.month, "月", today.day, "日", today.hour,"時", today.minute, "分", today.second, "秒", today.microsecond, "マイクロ秒")

        jsonobj[self._today.month] = []

        logging.debug('AA')
        return jsonobj

    def main(self):
        logging.debug('VV')

        logging.debug(self._jsonfile)
        jsonobj = self.load_JSON(self, self._jsonfile)
        # logging.debug(json['01'])

        jsonobj = self.add_JSON(self, jsonobj)

        json.dump(jsonobj, open(self._jsonfile, 'w'), indent=4)

        logging.debug('AA')

    def __init__(self):
        logging.debug('VV')
        logging.debug('AA')


if __name__ == "__main__":
    # ダブルクリックなどで実行された場合に”__name__”に”__name__”と入るのでここが実行される。
    logging.debug('VV')
    myClass = LoadAndAddJSON
    myClass.main(myClass)
    logging.debug('AA')
