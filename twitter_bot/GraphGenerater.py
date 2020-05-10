from collections import OrderedDict
import datetime
from datetime import timedelta
import json
import logging
import os
import twitter_bot

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import numpy as np
from matplotlib import rcParams

from mpl_toolkits.axes_grid1 import make_axes_locatable

    # https://docs.python.org/ja/3/library/datetime.html#
    # _today = datetime.datetime.now().isoformat()
    # _today 2019-10-17T23:11:56.338690

_today = datetime.datetime.now()
#_today = datetime.date(2020,1,1)
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

class GraphGenerater:
    '''20XX_SensorData.jsonから昨日のセンサーデータを取り出す．\n
        昨日が月末であれば，先月分のセンサーデータ一ヶ月分を取り出す．\n
        昨日が年末であれば，一年分のセンサーデータを取り出す．\n

        取り出されたデータでグラフを作成する．
    '''
    
    # ログレベルのフォーマット Log.txtファイルに出力
    logging.basicConfig(level=logging.DEBUG, filename='./Log.txt', filemode='w',format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

    _jsonfile = './{}_SensorData.json'.format(_yesterday.year)
    '''昨日のセンサーデータの入ったjsonファイル名を指定 "2019_SensorData.json"と先頭に年が入る
    '''

    def _IsYesterday(self):
        '''
            昨日は去年か，先月か，同じ月の機能かの判定パターンを入れる．\n
        
        Returns:
            str: 'yesterday'・・・同じ月の昨日,'lastMonth'・・・先月,'lastYear'・・・去年
        '''
        logging.debug('VV')
        
        # 昨日は年末か月末か昨日かの文字列を入れる
        _ = ''

        # 今日の日付と昨日の日付を比較
        # 年は同じ，月は同じ，今日の日付が大きい
        if (_today.year == _yesterday.year and _today.month == _yesterday.month and _today.day > _yesterday.day):
            _ = 'yesterday'
        # 年は同じ，昨日
        elif (_today.year == _yesterday.year and _today.month > _yesterday.month):
            _ = 'lastMonth'
        # 昨年
        elif (_today.year > _yesterday.year):
            _ = 'lastYear'
        
        #_ = 'yesterday'
        #_ = 'lastMonth'
        #_ = 'lastYear'
        
        logging.debug('AA')

        return _

    def _Load_JSON(self, jsonFile):
        '''_jsonfileをよみだす
        
        Args:
            jsonFile ([str]): [_jsonfile・・・センサーデータが記載されたファイル名]
        
        Returns:
            [jsonobj]: [_jsonfileを読みだしたもの]
        '''        

        logging.debug('VV')
        return json.load(open(jsonFile, 'r'))

    def RepackSensordata(self):
        '''_jsonfile(20XX_SensorData.json)から昨日のセンサーデータを取り出す．\n
        昨日が月末であれば，先月分のセンサーデータ一ヶ月分を取り出す．\n
        昨日が年末であれば，一年分のセンサーデータを取り出す．\n\n

        Returns:
            [type]: [description]
        '''

        logging.debug('VV')

        try:
            jsonobj = self._Load_JSON(self._jsonfile)
            
        except FileNotFoundError:
            logging.debug('FileNotFound:' + self._jsonfile)
            return

        #logging.debug(type(jsonobj))

        mo = str(_yesterday.month)
        # mo = "1"

        today = str(_yesterday.day)
        #today = "1"

        # センサーデータを一月ごとに保管用
        month_sensorData = {}

        # 今日の日付と昨日の日付を比較
        # 年は同じ
        yesterdayPttn = self._IsYesterday()

        # 昨日は昨年
        if (yesterdayPttn == 'lastYear'):
            # 一年分のデータを詰め込み
            month_sensorData = jsonobj

        # 昨日は月末
        elif (yesterdayPttn == 'lastMonth'):
            # 昨日の月分のセンサーデータリストを月Mapに詰め込み
            month_sensorData.setdefault(mo, {})
            month_sensorData[mo] = jsonobj[mo]

        # 昨日
        elif (yesterdayPttn == 'yesterday'):
            #logging.debug(jsonobj[mo][today])
            #logging.debug('---')

            # 昨日のセンサーデータリストを月Mapに詰め込み
            month_sensorData.setdefault(mo, {}).setdefault(today,{})
            month_sensorData[mo][today] = jsonobj[mo][today]

        logging.debug('AA')

        return month_sensorData

    def GenGraph(self, sensorDataList):
        '''[受け取ったデータでグラフを作成する．]
        
        Args:
            sensorDataList ([dict]): [昨日，先月，去年のセンサーデータリスト]
        '''        

        logging.debug('VV')

        # sensorDataListからCO2の値を月別日別で取り出し，sensorCO2Listへ入れる．
        monthList = sensorDataList.keys()
        dayList = []
        sensorCO2List=[]
        #logging.debug('---')

        for mo in monthList:
            dayList.append(sensorDataList[mo].keys())
            for day in sensorDataList[mo].keys():
                sensorCO2List.append([int(_) for _ in sensorDataList[mo][day]['CO2']])
        logging.debug(sensorCO2List)
        #logging.debug('---')
        
        #表をファイルに保存
        saveFileName = 'graph.png'
        
        # グラフ中のタイトル
        graphTitle = ''

        # 今日の日付と昨日の日付を比較
        # 年は同じ
        yesterdayPttn = self._IsYesterday()

        tmp_year =_yesterday.year
        tmp_mo = _yesterday.month
        tmp_today = _yesterday.day

        # 表の表示サイズを固定 figsize=(width, height)
        fig, ax = plt.subplots(figsize=(8,6))

        # グラフのタイトルと，保存ファイル名に年月日をつける
        # 昨日は昨年
        if (yesterdayPttn == 'lastYear'):
            saveFileName = './{}-CO2濃度.png'.format(tmp_year)
            graphTitle = '{} CO2濃度　PPM'.format(tmp_year)
                        
            # 表の表示サイズを固定 figsize=(width, height)
            fig, ax = plt.subplots(figsize=(8, 30))

        # 昨日は月末
        elif (yesterdayPttn == 'lastMonth'):
            saveFileName = './Monthly-CO2濃度.png'
            graphTitle = '{}/{MM:02} CO2濃度　PPM'.format(tmp_year, MM=tmp_mo)

        # 今日の昨日は一日前
        elif (yesterdayPttn == 'yesterday'):
            saveFileName = './Daily-CO2濃度.png'
            graphTitle = '{}/{MM:02}/{DD:02} CO2濃度　PPM'.format(tmp_year, MM=tmp_mo, DD=tmp_today)

        # https://qiita.com/yniji/items/3fac25c2ffa316990d0c
        # 日本語を利用する場合のFont指定 <個別に>
        #igfont = {'family': 'IPAexGothic'}
        # plt.title('title',**igfont)

        # 日本語を利用する場合のFont指定 <全体>
        rcParams['font.family'] = 'sans-serif'
        rcParams['font.sans-serif'] = ['MigMix 2P','IPAPGothic']

        # 図の諸々設定
        #  気温
        # plt.imshow(rbm, cmap='RdBu_r',extent=(0, 48, 0, 1),aspect=1, vmin=-10, vmax=40)

        # 気圧
        # plt.imshow(rbm, cmap='RdBu_r',extent=(0, 48, 0, 1),aspect=1, vmin=950, vmax=1080)

        # 湿度
        # plt.imshow(rbm, cmap='RdBu_r',extent=(0, 48, 0, 1),aspect=1, vmin=0, vmax=100)

        # CO2
        im = ax.imshow(sensorCO2List, cmap='RdBu_r', extent=(0, 48, len(sensorCO2List), 0),  vmin=300, vmax=1600)
        ax.set_title(graphTitle)
        ax.set_xlabel('時間 (一時間にデータを2回取得なので48回　要調整)')
        # ax.set_xticklabels(farmers)
        # ax.set_yticklabels(vegetables)
        ax.set_ylabel('日')
        #plt.legend('凡例')

        # X軸の開始～終わり
        ax.set_xlim(0, 48)
        #ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(2))

        # Y軸の開始～終わり
        ax.set_ylim(0,len(sensorCO2List))

        #カラーバー colorbarの調整方法を調べてたらいつのまにか2時間経ってた 難しすぎでしょ 
        divider = make_axes_locatable(ax)
        # cax = divider.append_axes(position = 'right',size='2%', pad=0.1)
        cax = divider.append_axes(position = 'right',size='2%', pad='5%')
        plt.colorbar(im, cax=cax,orientation='vertical')
        
        #グリッド
        ax.grid()

        fig.savefig(saveFileName)
        #plt.show()

        logging.debug('AA')
        return saveFileName

    def UpdateTweetWithImage(self, msg, img):
        '''[Twitter_botでTweet]
        
        Args:
            sendmsg ([str]): [Tweetメッセージ]
        '''        
        _ = twitter_bot.Twitter_bot()
        _.UpdateTweetWithImg(msg,img)

    def main(self):
        '''[summary]
        '''

        sensordata = self.RepackSensordata()
        #logging.debug(sensordata)
        savefile = self.GenGraph(sensordata)
        
        # センセーのデータをTweet
        self.UpdateTweetWithImage('#CO2 concentration',savefile)

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
    # ダブルクリックなどで実行された場合に”__name__”に”__name__”と入るのでここが実行される
    logging.debug('VV')
    myclass = GraphGenerater()
    myclass.main()
    del myclass
    logging.debug('AA')
