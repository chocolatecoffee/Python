import sys
import logging
import os
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as tkmsgbox
import getMD5

logging.basicConfig(level=logging.DEBUG,filename='Log.txt',format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

testFile="C:\\Windows\\explorer.exe"
root = tk.Tk()
getmd5=getMD5.getMD5()


class CheckMd5(tk.Frame):
    '''選択されたファイルのMD5を算出します。'''

    def __init__(self, master=None):
        super().__init__(master)
        master.title('CheckMd5')
        master.geometry('400x400')

        self.pack()
        self.create_widgets()

    def create_widgets(self):
        '''ウィジェットの内容を構成，表示'''
        v = tk.IntVar()
        
        tk.Label(self, text='\n',).pack()
        tk.Label(self, text='MD5を確認するファイルを選択').pack()

        self.entry_File = tk.Entry(self,width=35)
        self.entry_File.insert(tk.END, testFile)
        self.entry_File.pack()
        tk.Button(self, text='ファイルを参照', width=25,command=self.btn_BrowsFile).pack()
        tk.Button(self, text='MD5 算出', width=25, command=lambda: app.btn_CheckMD5(self.entry_File.get())).pack()

        tk.Label(self, text='\n',).pack()
        tk.Label(self, text='MD5結果').pack()
        self.entry_outPutM5 = tk.Entry(self, width=35)
        self.entry_outPutM5.insert(tk.END, 'MD5を出力します。')
        self.entry_outPutM5.pack()

    def btn_BrowsFile(self):
        '''ファイルを参照ボタンを押した際の挙動'''
        logging.debug('Click btn_BrowsFile VV')

        fTyp = [("","*")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        filepath = filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
        #self.entry_File.set(filepath)
        self.entry_File.delete(0, tk.END)
        self.entry_File.insert(tk.END, filepath)

        logging.debug('Click btn_BrowsFile AA')

    def btn_CheckMD5(self,str_file):
        '''MD5を算出する'''
        logging.debug('Click btn_CheckMD5 VV')
        if len(str_file) <= 0:
            '''文字列がない場合を記述したい'''
            print(len(str_file))

        logging.debug(str_file)

        #算出下MD5をMD5結果へ出力
        str_MD5=getmd5.checkMd5(str_file)
        self.entry_outPutM5.delete(0, tk.END)
        self.entry_outPutM5.insert(tk.END, str_MD5)

        logging.debug('Click btn_CheckMD5 AA')

app = CheckMd5(master=root)
app.mainloop()