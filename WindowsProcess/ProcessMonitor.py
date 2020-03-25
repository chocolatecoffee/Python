# -*- coding: utf-8 -*-
# https://github.com/mhammond/pywin32

import win32con
import win32api
import win32security

import wmi
import sys
import os
import datetime
import time

import logging
import json

# ログレベルのフォーマット Log.txtファイルに出力
logging.basicConfig(level=logging.DEBUG, filename='./Log.txt',
                    format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s', filemode='w')

_JSONFILE = './Settings.json'


class ProcessMonitor:

    def get_process_privileges(self, pid):

        logging.debug('VV')
        priv_list = []

        try:
            # 対象のプロセスへのハンドルを取得
            hproc = win32api.OpenProcess(
                win32con.PROCESS_QUERY_INFORMATION, False, pid)

            # メインのプロセストークンを開く
            htok = win32security.OpenProcessToken(hproc, win32con.TOKEN_QUERY)

            # 有効化されている権限のリストを取得
            privs = win32security.GetTokenInformation(
                htok, win32security.TokenPrivileges)

            # 権限をチェックして、有効化されているものだけを出力するループ

            for priv_id, priv_flags in privs:

                # 権限が有効化されているかチェック
                if priv_flags == 3:
                    priv_list.append(
                        win32security.LookupPrivilegeName(None, priv_id))

        except Exception as ex:
            priv_list.append('N/A')
            logging.debug(ex)

        logging.debug('AA')

        return '|'.join(priv_list)

    def Main(self):
        logging.debug('VV')
        jsonobj = json.load(open(_JSONFILE, 'r'))

        # WMIインタフェースのインスタンス化
        c = wmi.WMI()

        # プロセス監視の開始
        process_watcher = c.Win32_Process.watch_for('creation')

        while True:
            try:
                new_process = process_watcher()

                proc_owner = new_process.GetOwner()
                proc_owner = '{}-{}'.format(proc_owner[0], proc_owner[2])
                create_date = new_process.CreationDate

                executable = new_process.ExecutablePath
                mdline = new_process.CommandLine
                pid = new_process.ProcessId
                parent_pid = new_process.ParentProcessId

                privileges = self.get_process_privileges(self, pid)

                # process_log_message = '%s,%s,%s,%s,%s,%s,%s' % (create_date, proc_owner, executable, cmdline, pid, parent_pid, privileges)

                # process_log_message = '{},{},{},{},{},{}'.format(str(proc_owner), str(
                #    executable), str(mdline), str(pid), str(parent_pid), str(privileges))

                print('{}--{}:{}:{}'.format(str(create_date), str(executable), str(
                    pid), str(parent_pid)))

                # logging.debug(process_log_message)

            except Exception as ex:
                logging.debug(ex)

                pass


if __name__ == '__main__':
    logging.debug('VV')
    myClass = ProcessMonitor
    myClass.Main(myClass)
    logging.debug('AA')
