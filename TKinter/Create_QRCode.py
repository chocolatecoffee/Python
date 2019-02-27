import sys
import logging
import os
import qrcode
import PIL.ImageTk as pilimg
import tkinter as tk
import tkinter.messagebox as tkmsgbox

logging.basicConfig(level=logging.DEBUG, filename='Log.txt',
                    format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

root = tk.Tk()

class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        master.title('--QRCode Maker--')
        master.geometry('400x400')

        self.pack()
        self.create_widgets()

    def create_widgets(self):
        '''ウィジェットの内容を構成，表示'''

        tk.Label(self, text='URL').pack()

        self.entry_url = tk.Entry(self, width=25)
        self.entry_url.insert(tk.END, 'https://www.yahoo.co.jp/')
        self.entry_url.pack()

        tk.Button(self, text='QRCode作成', command=lambda: app.btn_create_QRCode(
            self.entry_url.get())).pack()

        tk.Button(self, text='保存', command=lambda: app.btn_save_QRCode(
            self.entry_url.get())).pack()

        self.canvas = tk.Canvas(self, width='250', height='250', bg='white')
        self.canvas.pack()

    def btn_save_QRCode(self, str_url):
        '''QRCodeを画像として保存・・・エクスプローラを開いて保存します．'''

        logging.debug('btn_saveQRCode VV')
        logging.debug('btn_saveQRCode AA')

    def btn_create_QRCode(self, str_url):
        '''QRCode作成 ボタンの処理・・・canvasにQRCodeを貼り付ける'''

        #　global QRimgをここで宣言しないとQRCodeがはりつきません．
        global QRimg
        if len(str_url) > 0:

            QRimg = pilimg.PhotoImage(self.create_QRCode(str_url))
            f = ('FixedSys, 12')
            self.canvas.delete('all')
            self.canvas.create_text(125, 15, text=str_url, font=f)
            self.canvas.create_image(125, 125, image=QRimg, anchor=tk.CENTER)

    def create_QRCode(self, str_url):
        '''QRCodeデータを作成する'''

        qr = qrcode.QRCode(
            # QRコードの大きさ(バージョン)。Noneで自動設定(1～22)。数値指定しても必要なら自動で大きくなる
            version=None,
            # 誤り訂正レベルL,M,Q,H
            # error_correction=qrcode.constants.ERROR_CORRECT_M,
            # サイズを何倍にするか。1ならdot-by-dot(px)
            box_size=3,
            # 認識用余白(最低4)
            border=4,
        )
        qr.add_data(str_url)
        qr.make(fit=True)
        return qr.make_image()


app = Application(master=root)
app.mainloop()
