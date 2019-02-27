# TKinterTest

import sys
import logging
import os
import tkinter as tk
import tkinter.messagebox as tkmsgbox

logging.basicConfig(level=logging.DEBUG, filename='Log.txt',
                    format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

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


app = Application(master=root)
app.mainloop()
