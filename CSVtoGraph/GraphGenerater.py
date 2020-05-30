import CsvLoader
import logging

import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.axes_grid1.inset_locator import inset_axes


class GraphGenerater:

    # ログレベルのフォーマット Log.txtファイルに出力
    logging.basicConfig(level=logging.DEBUG, filename='Log.txt', filemode='w',
                        format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

    def AdjustData(self, unadjust_data):
        '''[CSVのファイル内容をColumnHeader、RowHeader、Fieldに分ける]
            CSVの表は以下の形を取る必要がある。"X"は読み飛ばされる。
            X   A   B   C
            1   a   b   c
            2   d   e   f
            3   g   h   i

            ColumnHeaderに[AB,C]
            RowHeaderに[1,2,3]
            Fieldに[[a,b,c][d,e,f][g,h,i]]と入る

        Args:
            unadjust_data ([str]): [CSVFilePath]

        Returns:
            [List]: [ColumnHeader:CSVファイルの先頭1行目]
            [List]: [RowHeader:CSVファイルの1列目]
            [List]: [Field:ColumnHeader,RowHeader以外の部分]
        '''
        ColumnHeader = []
        RowHeader = []
        Field = []

        itr_csvdata = iter(unadjust_data)
        csvdata = next(itr_csvdata)
        # ヘッダーの先頭文字は読み飛ばす
        ColumnHeader = csvdata[1:]

        for csvdata in itr_csvdata:
            temp = []
            RowHeader.append(csvdata[0])
            for f in csvdata[1:]:
                temp.append(int(f))
            Field.append(temp)

        return ColumnHeader, RowHeader, Field

    def GenGraph(self, unadjust_data, saveFileName):
        '''[CSVファイルから図を出力する。]

            CSVの表は以下の形を取る必要がある。
            X   A   B   C
            1   a   b   c
            2   d   e   f
            3   g   h   i

            ColumnHeaderに[AB,C]
            RowHeaderに[1,2,3]
            Fieldに[[a,b,c][d,e,f][g,h,i]]と入る

        Args:
            unadjust_data ([type]): [CSVFilePath]
            saveFileName ([type]): [output path/picturename]
        '''

        # Axes.set_xlabel
        # X軸ラベル
        # Axes.set_ylabel
        # Y軸ラベル
        # Axes.set_title
        # グラフのタイトル
        # Axes.set_xlim
        # X軸の描画範囲
        # Axes.set_ylim
        # Y軸の描画範囲
        # Axes.set_xticks
        # X軸の目盛り。リストで指定する。
        # Axes.set_xticklabels
        # X軸の目盛りの表記。リストで指定する。
        # Axes.set_yticks
        # Y軸の目盛り。リストで指定する。
        # Axes.set_yticklabels
        # Y軸の目盛りの表記。リストで指定する。
        # Axes.grid
        # 目盛りに合わせてグリッドを表示する。

        ColumnHeader, RowHeader, Field = self.AdjustData(unadjust_data)

        # 表のタイトル
        graphTitle = 'サンプルタイトル'

        # XLabael
        xLabel = 'X軸'

        # Ylabel
        yLabel = 'Y軸'

        # 日本語を利用する場合のFont指定 <全体>
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['MigMix 2P', 'IPAPGothic']

        # 表の表示サイズを固定 figsize=(width, height)
        # fig, ax = plt.subplots(figsize=(8, 6))
        fig, ax = plt.subplots(figsize=(10, 10))

        # im = ax.imshow(Field, cmap='hot', extent=(
        #    0, len(ColumnHeader), len(RowHeader), 0), vmin=0, vmax=10000)

        arryField = np.array(Field)

        #im = ax.pcolormesh(arryField, cmap='GnBu')
        im = ax.imshow(arryField, cmap="GnBu")

        # 表,XYの軸タイトル
        ax.set_title(graphTitle)
        ax.set_xlabel(xLabel)
        ax.set_ylabel(yLabel)

        # X軸の開始～終わり
        # ax.set_xlim(0, 99)

        # X軸要素名
        ax.set_xticklabels(ColumnHeader)
        ax.set_xticks(np.arange(len(ColumnHeader)), minor=False)

        # X軸の数値を何個飛ばしで表示するか
        # ax.xaxis.set_major_locator(ticker.MultipleLocator(base=1))
        # ax.xaxis.set_major_locator(ticker.MaxNLocator(len(ColumnHeader)))

        # Y軸の開始～終わり
        # ax.set_ylim()

        # Y軸要素名
        ax.set_yticklabels(RowHeader)
        ax.set_yticks(np.arange(len(RowHeader)), minor=False)

        # Y軸の数値を何個飛ばしで表示するか
        # ax.yaxis.set_major_locator(ticker.MultipleLocator(base=2))
        # ax.yaxis.set_major_locator(ticker.MaxNLocator(len(RowHeader)))

        # グリッド
        # ax.grid()

        # 凡例
        # bbox_to_anchorをうまく調整しないと見切れる
        ax_colorbar = inset_axes(ax, width='50%', height='3%', loc='upper center', bbox_to_anchor=(
            0, -1.3, 1, 1), bbox_transform=ax.transAxes, borderpad=1)
        plt.colorbar(im, cax=ax_colorbar,
                     orientation='horizontal', label='凡例')

        # Y軸要素を傾ける
        plt.setp(ax.get_yticklabels(), rotation=45, ha="right",
                 rotation_mode="anchor")

        # メッシュの上に数値を描画
        for i in range(len(RowHeader)):
            for j in range(len(ColumnHeader)):
                # logging.debug('i= {}'.format(i))
                # logging.debug('j= {}'.format(j))
                # logging.debug('arry {} '.format(arryField[i, j]))
                text = ax.text(j, i, arryField[i, j],
                               ha="center", va="center", color="m")

        # fig.tight_layout()
        fig.savefig(saveFileName)
        # plt.show()

    def Main(self):
        logging.debug('VV')
        loader = CsvLoader.CsvLoader()
        # sampledata
        csvfile = './sample_04.tsv'

        # 保存ファイル名
        saveFileName = './test.png'

        self.GenGraph(loader.LoadTSV(csvfile), saveFileName)

        logging.debug('outputs:' + saveFileName)

        logging.debug('AA')

    def __new__(cls):

        logging.debug('__new__')
        self = super().__new__(cls)
        return self

    def __init__(self):

        logging.debug('__init__')

    def __del__(self):

        logging.debug('__del__')


if __name__ == "__main__":
    logging.debug('VV')
    myclass = GraphGenerater()
    myclass.Main()
    del myclass
    logging.debug('AA')
