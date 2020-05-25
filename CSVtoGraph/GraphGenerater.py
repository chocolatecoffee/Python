import logging
import CsvLoader

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rcParams
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# ログレベルのフォーマット Log.txtファイルに出力
logging.basicConfig(level=logging.DEBUG, filename='Log.txt', filemode='w',
                    format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')


class GraphGenerater:

    _csvfile = './sample_00.tsv'

    def AdjustData(self, unadjust_data):
        '''[summary]

        Args:
            unadjust_data ([type]): [description]

        Returns:
            [type]: [description]
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

    def GenGraph(self, unadjust_data):
        '''[summary]

        Args:
            unadjust_data ([type]): [description]

        Returns:
            [type]: [description]
        '''

        ColumnHeader, RowHeader, Field = self.AdjustData(unadjust_data)

        # 保存ファイル名
        saveFileName = './test.png'

        # 表のタイトル
        graphTitle = 'サンプルタイトル'

        # 日本語を利用する場合のFont指定 <全体>
        rcParams['font.family'] = 'sans-serif'
        rcParams['font.sans-serif'] = ['MigMix 2P', 'IPAPGothic']

        # 表の表示サイズを固定 figsize=(width, height)
        # fig, ax = plt.subplots(figsize=(8, 6))
        fig, ax = plt.subplots(figsize=(10, 10))

        im = ax.imshow(Field, cmap='hot', extent=(
            0, len(ColumnHeader), len(RowHeader), 0), vmin=0, vmax=10000)

        # 表タイトル,XYの軸名
        ax.set_title(graphTitle)
        ax.set_xlabel('X軸名')
        ax.set_ylabel('Y軸名')

        # X軸の開始～終わり
        ax.set_xlim(0, len(ColumnHeader))
        # X軸の数値を何個飛ばしで表示するか
        ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(base=10))

        # Y軸の開始～終わり
        ax.set_ylim(0, len(RowHeader))
        # Y軸の数値を何個飛ばしで表示するか
        ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(base=10))

        # グリッド
        # ax.grid()

        # 凡例
        # ax_colorbar = inset_axes(ax, width = '75%', height = '40%', loc = 'upper center', bbox_to_anchor = (0, -7, 1, 1),bbox_transform = ax.transAxes,)
        # fig.colorbar(im, cax=ax_colorbar, orientation='horizontal', label='凡例：')

        fig.savefig(saveFileName)
        # plt.show()

        logging.debug('AA')
        return saveFileName

    def Main(self):
        logging.debug('VV')
        loader = CsvLoader.CsvLoader()
        savefile = self.GenGraph(loader.LoadTSV(self._csvfile))
        logging.debug('outputs:' + savefile)

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
    myclass = GraphGenerater()
    myclass.Main()

    logging.debug('AA')
