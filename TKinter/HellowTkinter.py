# TKinterTest

import sys
import logging
import os
import tkinter as tk
import tkinter.messagebox as tkmsgbox

logging.basicConfig(level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')

root = tk.Tk()


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        master.title('Window Title')
        master.geometry('400x300')

        self.pack()
        self.create_widgets()

    def create_widgets(self):
        '''ウィジェットの内容を構成，表示'''

        # こういう書き方もあり PythonDoc…https://docs.python.org/ja/3/library/tkinter.html#a-simple-hello-world-program
        self.hi_there = tk.Button(self)
        self.hi_there['text'] = 'Hello World\n(click me)'
        self.hi_there['command'] = self.say_hi
        self.hi_there.pack()

        tk.Label(self, text='',
                 foreground='#00ff00', background='#000000').pack()

        tk.Label(self, text='入力入力',
                 foreground='#ff0000', background='#ffffff').pack(side='top')

        tk.Label(self, text='\n',
                 foreground='#00ff00', background='#000000').pack()

        self.entry_01 = tk.Entry(self, width=25)
        self.entry_01.insert(tk.END, 'entry_01,挿入する文字列')
        self.entry_01.pack()

        # lambdaで実行する場合,entry_01の内容を消す
        tk.Button(self, text='エントリーを消す',
                  command=lambda: self.entry_01.delete(0, tk.END)).pack()

        # entry_01の内容を showMessageへ渡す．
        tk.Button(self, text='bttn_01', width=25,
                  command=lambda: app.showMessage(self.entry_01.get())).pack()

        # Windowを終了する
        tk.Button(self, text='QUIT', fg='red',
                  command=self.master.destroy).pack()

        tk.Button(self, text='showDialog', width=25,
                  command=self.showDialog).pack()

    def say_hi(self):
        print('hi there, everyone!')

    def showMessage(self, str):
        tkmsgbox.showinfo('ダイアログのタイトル', str)
        tkmsgbox.showinfo('', len(str))

    def showDialog(self):
        '''「showDialog」ボタンが押されたら呼び出される関数'''

        # 普通のダイアログ
        tkmsgbox.showinfo('ダイアログのタイトル', self)

        # ワーニングなダイアログ
        tkmsgbox.showwarning('ダイアログのタイトル', 'ワーニングなダイアログ')

        # エラーな感じのダイアログ
        tkmsgbox.showerror('ダイアログのタイトル', 'エラーな感じのダイアログ')

        # YES/NOなダイアログ（YESがクリックされたら戻り値がtrue、NOならfalse）
        tkmsgbox.askyesno('ダイアログのタイトル', 'YES/NOなダイアログ')

        # リトライキャンセルダイアログ（リトライがクリックされたら戻り値がtrue、キャンセルならfalse）
        tkmsgbox.askretrycancel('ダイアログのタイトル', 'リトライキャンセルダイアログ')

        # OK/NOダイアログ（リトライがクリックされたら戻り値が'yes'、キャンセルなら'no'）
        tkmsgbox.askquestion('ダイアログのタイトル', 'OK/NOダイアログ')

        # OK/CANCELダイアログ（OKがクリックされたら戻り値がtrue、キャンセルならfalse
        tkmsgbox.askokcancel('ダイアログのタイトル', 'OK/CANCELダイアログ')


app = Application(master=root)
app.mainloop()
