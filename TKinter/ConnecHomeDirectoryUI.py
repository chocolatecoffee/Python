# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkmsgbox
import logging
import ConnectHomeDirectory


import logging
import json
import getpass
import unicodedata
import sys
import subprocess
import ldap3
import win32com.client
import ssl
import os
import time
from ldap3 import Server, Connection, Tls,ALL, NTLM, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, AUTO_BIND_NO_TLS, SUBTREE,SAFE_SYNC
from ldap3.core.exceptions import LDAPCursorError,LDAPBindError

# ログレベルのフォーマット Log.txtファイルに出力
logging.basicConfig(level=logging.DEBUG,filename='./Log_ConnectHomeDirectory.txt',format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s',filemode='w')

class ConnecHomeDirectoryUI(tk.Frame):
    homedrive = ConnectHomeDirectory.ConnectHomeDirectory()

    # messagebox.showinfo(タイトル, メッセージ内容)

    def EnterUserAndPassFromTK(self,userID,password):
        '''[summary]

        Returns:
            [type]: [description]
        '''

        logging.debug('VV')
        subprocess.run('chcp 65001', shell=True)
        try:
            # userID = input('Enter your V-CampusID > ')
            # password = getpass.getpass('Enter your V-Campus Password > ')
            while 1:
                cnt_zenkakuID = 0
                cnt_zenkakuPass = 0
                if len(userID) <= 0:
                    tkmsgbox.showinfo('', 'No ID has been entered.')
                    continue
                elif len(password) <= 0:
                    tkmsgbox.showinfo('','No Password has been entered.')
                    continue
                for char_userID in userID:
                    if unicodedata.east_asian_width(char_userID) != 'Na':
                        cnt_zenkakuID+=1
                for char_pass in password:
                    if unicodedata.east_asian_width(char_pass) != 'Na':
                        cnt_zenkakuPass+=1
                if cnt_zenkakuID > 0:
                    tkmsgbox.showinfo('','V-CampusID:Enter in half-width alphanumeric characters.')
                    continue
                elif cnt_zenkakuPass > 0:
                    tkmsgbox.showinfo('','Password:Enter in half-width alphanumeric characters.')
                    continue
                else:
                    break
                # logging.debug(userID)
                # logging.debug(password)
            
            logging.debug('AA')
            return userID,password
            
        except TypeError as exp:
            logging.exception(exp)

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title(u'Connect HomeDirectory')
        ttk.Style().theme_use('classic')
        self.pack()
        self.create_widgets()
        
    def create_widgets(self):

        self.master.resizable(False, False)
        frame1 = ttk.Frame(self, padding=(32))
        frame1.grid()

        label1 = ttk.Label(frame1, text='V-CVampus ID', padding=(5, 2))
        label1.grid(row=0, column=0, sticky='E')

        label2 = ttk.Label(frame1, text='Password', padding=(5, 2))
        label2.grid(row=1, column=0, sticky='E')

        # Username Entry
        username = tk.StringVar()
        username_entry = ttk.Entry(frame1,textvariable=username, width=20)
        username_entry.grid(row=0, column=1)

        # Password Entry
        password = tk.StringVar()
        password_entry = ttk.Entry(frame1,textvariable=password, width=20, show='*')
        password_entry.grid(row=1, column=1)

        frame2 = ttk.Frame(frame1, padding=(0, 5))
        frame2.grid(row=2, column=1, sticky='W')


        button2 = ttk.Button(frame2, text='QUIT', command=self.master.destroy)
        button2.pack(side='left')

        button1 = ttk.Button( frame2, text='OK', command= lambda: self.EnterUserAndPassFromTK(username.get(), password.get()))
        button1.pack(side='left')

if __name__ == "__main__":
    # ダブルクリックなどで実行された場合に”__name__”に”__name__”と入るのでここが実行される。
    logging.debug('VV')

    ConnecHomeDirectoryUI(master = tk.Tk()).mainloop()
    
    logging.debug('AA')
