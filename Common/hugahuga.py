import logging
import json

#　参考
# https://qiita.com/KEINOS/items/ea4bda15506bbd3e6913

# ログレベルのフォーマット Log.txtファイルに出力
logging.basicConfig(level=logging.DEBUG, filename='.\\Log.txt',
                    format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')


class hugahuga:

    '''adsa'''

    _jsondata = "..\\Settings_JSON\\2019_SensorData.json"
    '''asd'''

    def load_JSON(self, data_json):
        '''JSONの読み取り jsonを読み取る
        '''
        # logging.debug('VV')

        # Json読み取り
        with open(data_json, mode='r', encoding='utf-8') as obj_jsonfile:
            jsonFileData = json.load(obj_jsonfile)

        # logging.debug('AA')
        return jsonFileData

    def addData_JSON(self, jsonFileData):
        '''sonへ追記
        '''
        # logging.debug('VV')
        entry = {'': '', '': ''}
        jsonFileData.append(entry)
        json.dump(feeds, json)

        # logging.debug('AA')

    def __init__(self):
        '''asd'''

        logging.debug('VV')
        logging.debug('AA')

    def main(self):
        '''asd'''

        logging.debug('VV')
        logging.debug('AA')


if __name__ == "__main__":
    # ダブルクリックなどで実行された場合に”__name__”に”__name__”と入るのでここが実行される。
    logging.debug('VV')
    myClass = hugahuga
    myClass.main(myClass)
    logging.debug('AA')
