from collections import OrderedDict
import datetime
from datetime import timedelta
import json
import logging
import os

import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.axes_grid1 import make_axes_locatable

# ログレベルのフォーマット Log.txtファイルに出力
logging.basicConfig(level=logging.DEBUG, filename='./Log.txt', filemode='w',format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

# https://docs.python.org/ja/3/library/datetime.html#
# _today = datetime.datetime.now().isoformat()
# _today 2019-10-17T23:11:56.338690

_today = datetime.datetime.now()
'''datetime obj "Today" '''

_yesterday = _today - timedelta(days=1)
'''datetime obj "yesterday" '''

_tomorrow = _today + timedelta(days=1)
'''datetime obj "tomorrow" '''

 # _today.year
 # _today.month
 # _today.day
 # _today.hour
 # _today.minute
 # _today.weekday

class GrafGenerater:
    '''20XX_SensorData.jsonから昨日のセンサーデータを取り出す．\n
        昨日が月末であれば，先月分のセンサーデータ一ヶ月分を取り出す．\n
        昨日が年末であれば，一年分のセンサーデータを取り出す．\n

        取り出されたデータでグラフを作成する．
    '''

    _jsonfile = './{}_SensorData.json'.format(_yesterday.year)
    '''昨日のセンサーデータの入ったjsonファイル名を指定 "2019_SensorData.json"と先頭に年が入る
    '''

    def _load_JSON(self, jsonfile):
        '''_jsonfileをよみだす
        
        Args:
            _jsonfile ([type]): [description]
        '''        
        logging.debug('VV')

        return json.load(open(jsonfile, 'r'))

    def repackSensordata(self):
        '''20XX_SensorData.jsonから昨日のセンサーデータを取り出す．\n
        昨日が月末であれば，先月分のセンサーデータ一ヶ月分を取り出す．\n
        昨日が年末であれば，一年分のセンサーデータを取り出す．\n
        
        Returns:
            [dict]: 
        '''

        logging.debug('VV')

        try:
            jsonobj = self._load_JSON(self, self._jsonfile)
            
        except FileNotFoundError:
            logging.debug('FileNotFound:' + self._jsonfile)
            return

        #logging.debug(type(jsonobj))

        # 一日ごとのセンサーデータ保管用
        days_sensordata = []

        # 一日ごとのセンサーデータを一月ごとに保管用
        month_sensordata = {}

        # 今日の日付と昨日の日付を比較
        # 年は同じ
        #if ( _today.year == _yesterday.year):
        if ( _today.year == 2018):

            # 月は同じ
            if (_today.month == _yesterday.month):
            #if (_today.month == 11):

                # 今日の昨日は一日前
                if (_today.day > _yesterday.day):

                    #昨日の表を作成
                    logging.debug('yesterday')
                    # logging.debug(len(jsonobj[str(_yesterday.month)]))
                    # logging.debug(type(jsonobj[str(_yesterday.month)]))

                    for sensordata in jsonobj[str(_yesterday.month)]:
                        # logging.debug(sensordata['dd'])
                        # 昨日の日と一致する日付のセンサーデータをリストに詰め込み
                        if (sensordata['dd'] == str(_yesterday.day)):
                            # logging.debug(sensordata['dd'])
                            days_sensordata.append(sensordata)

                    # 昨日のセンサーデータリストを月Mapに詰め込み
                    month_sensordata.setdefault(str(_yesterday.month),days_sensordata)

                else:
                    # プログラムのトリガーされる時間からこの条件はない
                    logging.debug('Today!?')

            else:
                #先月の表を作成 (1ヶ月分)
                logging.debug('last month')

                # 昨日のセンサーデータリストを月Mapに詰め込み
                month_sensordata.setdefault(str(_yesterday.month),jsonobj[str(_yesterday.month)])

        else:
            #去年一年の表を作成(12ヶ月分)
            logging.debug('last year')

            month_sensordata=jsonobj

        logging.debug('AA')

        return month_sensordata

    def TEST_genGraf(self):
        ax = plt.subplot(111)
        ax.grid(False)
        im = ax.imshow(np.random.randn(100).reshape((10, 10)))

        # create an axes on the right side of ax. The width of cax will be 5%
        # of ax and the padding between cax and ax will be fixed at 0.05 inch.
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.1)
        plt.colorbar(im, cax=cax)
        plt.show()
        #plt.savefig()

    def main(self):
        '''[summary]
        '''
        #repacked_sensordata = self.repackSensordata(self)
        # type(repacked_sensordata)
        self.TEST_genGraf(self)

    def __init__(self):
        ''''''


if __name__ == "__main__":
    # ダブルクリックなどで実行された場合に”__name__”に”__name__”と入るのでここが実行される
    logging.debug('VV')
    myclass = GrafGenerater
    myclass.main(myclass)
    logging.debug('AA')
