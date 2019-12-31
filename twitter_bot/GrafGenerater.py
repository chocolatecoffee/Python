from collections import OrderedDict
import datetime
from datetime import timedelta
import json
import logging
import os

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import numpy as np
from matplotlib import rcParams

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

    def isYesterday(self):
        '''昨日は去年か，先月か，同じ月の機能かの判定パターン（yesterdayPattern）を入れる．\n
            'yesterday'・・・同じ月の昨日\n
            'lastMonth'・・・先月\n
            'lastYear'・・・去年\n
        
        Returns:
            [type]: [String]
        '''

        logging.debug('VV')

        yesterdayPattern = ''

        # 今日の日付と昨日の日付を比較
        # 年は同じ，月は同じ，今日の日付が大きい
        if (_today.year == _yesterday.year and _today.month == _yesterday.month and _today.day > _yesterday.day):
            yesterdayPattern = 'yesterday'
        # 年は同じ，昨日
        elif (_today.year == _yesterday.year and _today.month > _yesterday.month):
            yesterdayPattern = 'lastMonth'
        # 昨年
        elif (_today.year > _yesterday.year):
            yesterdayPattern = 'lastYear'

        logging.debug('AA')

        return yesterdayPattern

    def _load_JSON(self, jsonFile):
        '''_jsonfileをよみだす
        
        Args:
            _jsonfile ([type]): [description]
        '''        
        logging.debug('VV')

        return json.load(open(jsonFile, 'r'))

    def repackSensordata(self):
        '''_jsonfile(20XX_SensorData.json)から昨日のセンサーデータを取り出す．\n
        昨日が月末であれば，先月分のセンサーデータ一ヶ月分を取り出す．\n
        昨日が年末であれば，一年分のセンサーデータを取り出す．\n\n

        Returns:
            [type]: [description]
        '''

        logging.debug('VV')

        try:
            jsonobj = self._load_JSON(self, self._jsonfile)
            
        except FileNotFoundError:
            logging.debug('FileNotFound:' + self._jsonfile)
            return

        #logging.debug(type(jsonobj))

        # 一日ごとのセンサーデータ保管用
        days_sensorData = []

        # 一日ごとのセンサーデータを一月ごとに保管用
        month_sensorData = {}

        # 今日の日付と昨日の日付を比較
        # 年は同じ
        yesterdayPttn = self.isYesterday(self)

        # 昨日は昨年
        if (yesterdayPttn == 'lastYear'):
            # 一年分のデータを詰め込み
            month_sensorData = jsonobj

        # 昨日は月末
        elif (yesterdayPttn == 'lastMonth'):
            # 昨日のセンサーデータリストを月Mapに詰め込み
            month_sensorData.setdefault(str(_yesterday.month),jsonobj[str(_yesterday.month)])

        # 今日の昨日は一日前
        elif (yesterdayPttn == 'yesterday'):

            #昨日の表を作成
            # logging.debug(len(jsonobj[str(_yesterday.month)]))
            # logging.debug(type(jsonobj[str(_yesterday.month)]))

            for sensordata in jsonobj[str(_yesterday.month)]:
                # logging.debug(sensordata['dd'])
                # 昨日の日と一致する日付のセンサーデータをリストに詰め込み
                if (sensordata['dd'] == str(_yesterday.day)):
                    # logging.debug(sensordata['dd'])
                    days_sensorData.append(sensordata)

            # 昨日のセンサーデータリストを月Mapに詰め込み
            month_sensorData.setdefault(str(_yesterday.month),days_sensorData)

        logging.debug('AA')

        return month_sensorData

    def genGraphDataList(self, sensorData):
        '''[summary]
        
        Args:
            sensordata ([type]): [description]
        
        Returns:
            [type]: [description]
        '''

        logging.debug('VV')

        #graphList:ListにListを内包したものをグラフ描画のデータとする
        #graphList = [[-10, 0, 10, 20, 30,40], [40, 30, 20, 10, 0,-10], [-10, 0, 0, 0,0, 40], [1, 2, 3, 4, 5,6], [-10, 40, 0, 0, 0,0]]
        graphList = []

        # センサーデータを日にちごとに取りだす日にちの違い保管用
        strDay = ''
        
        #一日分のセンターデータ保管
        dailyDataList = []

        for key in sensorData.keys():
            for dailyData in sensorData[key]:

                sensorData_CO2= int(dailyData['CO2'])

                if(dailyData['dd'] == strDay):
                    dailyDataList.append(sensorData_CO2)

                elif (len(dailyDataList) == 0):
                    strDay = dailyData['dd']
                    dailyDataList.append(sensorData_CO2)

                else:
                    graphList.append(dailyDataList)
                    dailyDataList = []
                    strDay = dailyData['dd']
                    dailyDataList.append(sensorData_CO2)

        # リストの最終末分を入れる．
        if (len(dailyDataList) > 0):
            graphList.append(dailyDataList)

        logging.debug('AA')

        return graphList

    def genGraf(self,sensorDataList):
        '''[summary]
        
        Args:
            sensorDataList ([type]): [description]
        '''

        logging.debug('VV')

        # https://qiita.com/yniji/items/3fac25c2ffa316990d0c
        # 日本語を利用する場合のFont指定 <個別に>
        #igfont = {'family': 'IPAexGothic'}
        # plt.title('title',**igfont)

        # 日本語を利用する場合のFont指定 <全体>
        rcParams['font.family'] = 'sans-serif'
        rcParams['font.sans-serif'] = ['IPAPGothic', 'VL PGothic']

        # 表の表示サイズを固定
        plt.figure(figsize=(12, 5))

        #https://matplotlib.org/3.1.1/tutorials/colors/colormap-manipulation.html#sphx-glr-tutorials-colors-colormap-manipulation-py
        # 描画領域の確保だけ、グラフは何も描画されない
        #111の意味は、1行目1列の1番目という意味で、subplot(1,1,1)でも同じ.
        plt.subplot(111)

        # 図の諸々設定
        #  気温
        # plt.imshow(rbm, cmap='RdBu_r',extent=(0, 48, 0, 1),aspect=1, vmin=-10, vmax=40)

        # 気圧
        # plt.imshow(rbm, cmap='RdBu_r',extent=(0, 48, 0, 1),aspect=1, vmin=950, vmax=1080)

        # 湿度
        # plt.imshow(rbm, cmap='RdBu_r',extent=(0, 48, 0, 1),aspect=1, vmin=0, vmax=100)

        # CO2
        #plt.imshow(rbm, cmap='RdBu_r',extent=(0, 48, 0, 1),aspect=1, vmin=300, vmax=2000)
        #plt.imshow(graphList, cmap='RdBu_r', extent=(0, 48, 0, 1), aspect=1)
        plt.imshow(sensorDataList, cmap='RdBu_r', extent=(0, 48, len(sensorDataList), 0), aspect=1,vmin=300, vmax=1600)

        plt.title('CO2濃度　PPM')
        plt.xlabel('X軸ラベル 時間')
        # ax.set_xticklabels(farmers)
        # ax.set_yticklabels(vegetables)
        plt.ylabel('Y軸ラベル 年月日')
        #plt.legend('凡例')

        # X軸の開始～終わり
        plt.xlim(0,48)
        
        # Y軸の開始～終わり
        #plt.ylim(1, 0)
        plt.ylim(len(sensorDataList), 0)

        #カラーバー
        plt.colorbar()

        #表をファイルに保存
        # 2019/12/31-CO2 濃度.png _jsonfile = './{}_SensorData.json'.format(_yesterday.year)
        saveFileName = 'graph.png'
        
        # 今日の日付と昨日の日付を比較
        # 年は同じ
        yesterdayPttn = self.isYesterday(self)
        
        # 昨日は昨年
        if (yesterdayPttn == 'lastYear'):
            saveFileName = '{}'.format(_yesterday.year)

        # 昨日は月末
        elif (yesterdayPttn == 'lastMonth'):
            saveFileName = '{}-{}'.format(_yesterday.year,_yesterday.month)

        # 今日の昨日は一日前
        elif (yesterdayPttn == 'yesterday'):
            saveFileName = '{}-{}-{}'.format(_yesterday.year,_yesterday.month,_yesterday.day)

        plt.savefig('D://etc//Desktop//'+ saveFileName + '-CO2濃度.png')
        #plt.show()

        logging.debug('AA')

    def main(self):
        '''[summary]
        '''

        repacked_sensorData = self.repackSensordata(self)
        sensorDataList_CO2=self.genGraphDataList(self,repacked_sensorData)
        self.genGraf(self,sensorDataList_CO2)

    def __init__(self):
        ''''''

if __name__ == "__main__":
    # ダブルクリックなどで実行された場合に”__name__”に”__name__”と入るのでここが実行される
    logging.debug('VV')
    myclass = GrafGenerater
    myclass.main(myclass)
    logging.debug('AA')
