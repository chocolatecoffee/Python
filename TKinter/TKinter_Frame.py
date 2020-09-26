# TKinterTest

import sys
import logging
import os
import tkinter as tk
import tkinter.messagebox as tkmsgbox

logging.basicConfig(level=logging.DEBUG, filename='Log.txt', filemode='w',
                    format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')


class Application(tk.Frame):

    def main(self):
        '''[]
        '''
        logging.debug('VV')
        logging.debug('AA')

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.master.title(u"Software Title")
        self.master.geometry("400x400")
        #self.place(x=0, y=0)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack()
        #self.hi_there.place(x=20, y=20)

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack()
        #self.quit.place(x=50, y=50)

    def say_hi(self):
        id = self.EditBox_0.get()
        self.EditBox_0.insert(tk.END, id)

        if (len(id) == 0):
            tkmsgbox.showinfo('', 'insert ID')
        else:
            print(id)

    def __del__(self):
        '''[summary]
        '''
        logging.debug('__del__')


if __name__ == '__main__':
    logging.debug('VV')

    Application(master=tk.Tk()).mainloop()

    logging.debug('AA')
