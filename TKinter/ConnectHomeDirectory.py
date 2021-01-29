# -*- coding: utf-8 -*-
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

class ConnectHomeDirectory:

    _settings_json='./Settings.json'
    '''定数、文字列などを記述しておくJSONファイル'''

    _stngs = {}
    '''読みだされた設定情報（Settings.json）を保管用'''

    def LoadJSON(self,stngs):
        '''
        JSONの読み取り 指定されたJSONを読み取る.\n
        Returns:
            _settings_jsonで指定されているJSONオブジェクト
        '''
        try:
            # Json読み取り
            return json.load(open(stngs,'r', encoding='UTF-8'))
            
        except FileNotFoundError:
            logging.exception(self._settings_json + ' : FileNotFoundError')
            print('FileNotFound: Need ./Settings.json')

    def EnterUserAndPass(self):
        '''[summary]

        Returns:
            [type]: [description]
        '''

        logging.debug('VV')
        subprocess.run('chcp 65001', shell=True)
        try:
            userID = input('Enter your V-CampusID > ')
            password = getpass.getpass('Enter your V-Campus Password > ')
            while 1:
                cnt_zenkakuID = 0
                cnt_zenkakuPass = 0
                if len(userID) <= 0:
                    print('No ID has been entered.')
                    userID = input('Enter your V-CampusID > ')
                elif len(password) <= 0:
                    print('No Password has been entered.')
                    password = getpass.getpass('Enter your V-Campus Password > ')
                for char_userID in userID:
                    if unicodedata.east_asian_width(char_userID) != 'Na':
                        cnt_zenkakuID+=1
                for char_pass in password:
                    if unicodedata.east_asian_width(char_pass) != 'Na':
                        cnt_zenkakuPass+=1
                if cnt_zenkakuID > 0:
                    print('V-CampusID:Enter in half-width alphanumeric characters.')
                    userID = input('Enter your V-CampusID > ')
                elif cnt_zenkakuPass > 0:
                    print('Password:Enter in half-width alphanumeric characters.')
                    password = getpass.getpass('Enter your V-Campus Password > ')
                else:
                    break
            # logging.debug(userID)
            # logging.debug(password)
            
            logging.debug('AA')
            return userID,password
        except TypeError as exp:
            logging.exception(exp)


    def GetSrvConnectionWithSecure(self,id,password):
        '''[summary]

        Args:
            id ([type]): [description]
            password ([type]): [description]

        Returns:
            [type]: [description]
        '''

        try:
            logging.debug('VV')
            tls_configuration = Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1_2)
            server = Server('cr.rikkyo.ac.jp', port = 636, use_ssl = True, tls=tls_configuration,get_info=ALL)
            conn = Connection(server, 'cr\\'+id , password , check_names=True, read_only=True, auto_bind=True)
            # ユーザ、パスワードが違うとコネクションができないので’LDAPBindError’で終了させる
            conn.extend.standard.who_am_i()
            logging.debug('AA')
            return conn

        except LDAPBindError as exp:
            logging.exception(exp)
            print('Wrong ID or Password System Exit')
            sys.exit()

    def GetSrvConnection(self,id,password):
        '''[summary]

        Args:
            id ([type]): [description]
            password ([type]): [description]

        Returns:
            [type]: [description]
        '''

        try:
            logging.debug('VV')
            conn = Connection(Server('cr.rikkyo.ac.jp'), 'cr\\'+id , password , check_names=True, read_only=True, auto_bind=True)
            # ユーザ、パスワードが違うとコネクションができないので’LDAPBindError’で終了させる
            conn.extend.standard.who_am_i()
            logging.debug('AA')
            return conn

        except LDAPBindError as exp:
            logging.exception(exp)
            print('Wrong ID or Password System Exit')
            sys.exit()

    def SrchLdapSrv(self,conn,id):
        '''[summary]

        Args:
            conn ([type]): [description]
            id ([type]): [description]

        Returns:
            [type]: [description]
        '''

        logging.debug('VV')
        logging.debug(conn.extend.standard.who_am_i())
        conn.search('CN='+ id +',OU=People,OU=cr,DC=cr,DC=rikkyo,DC=ac,DC=jp',search_filter = '(&(|(objectclass=user)(objectclass=person)(sAMAccountName='+id+')(!(objectclass=computer))))',attributes = ['sAMAccountName','homeDrive','homeDirectory'], paged_size = 3)
        # conn.search('CN='+ id +',OU=People,OU=cr,DC=cr,DC=rikkyo,DC=ac,DC=jp','(objectclass=organizationalUnit)',attributes = ['homeDrive','homeDirectory'], paged_size = 3)
        # usually you don't need the original request (4th element of the return tuple)
        logging.debug('AA')
        return conn.entries

    def UnmountHomedrive(self):
        '''[summary]
        '''

        if os.path.exists('H:\\'):
            win32com.client.Dispatch('WScript.Network').RemoveNetworkDrive('H:', True, True)
            time.sleep(5)

    def MountHomedrive(self, userinf,id, password):
        '''[summary]

        Args:
            userinf ([type]): [description]
            id ([type]): [description]
            password ([type]): [description]
        '''

        # logging.debug(userinf)
        
        shell = win32com.client.Dispatch('WScript.Shell')
        Netshell = win32com.client.Dispatch('WScript.Network')
        Netshell.MapNetworkDrive(userinf['homeDrive'][0], userinf['homeDirectory'][0] ,False,'cr\\' + id, password)
        time.sleep(5)
        DesktopPath = shell.SpecialFolders('Desktop')
        shortcut = shell.CreateShortCut(DesktopPath +'\\ホームディレクトリ.lnk')
        shortcut.Targetpath = 'H:\\'
        shortcut.IconLocation = 'C:\\Windows\\System32\\Shell32.dll,150'
        shortcut.save()

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

    def Main(self,vid,vpass):
        '''[summary]
        '''

        logging.debug('VV')

        try:
            #設定情報読み出し
            self._stngs =  self.LoadJSON(self._settings_json)
            # ホームドライブを作成したいユーザのID、Passwordを入力,入力チェックをする。
            # id, password = self.EnterUserAndPass()
            id, password = self.EnterUserAndPassFromTK(vid,vpass)

            # ユーザのID、PasswordでLDAPサーバのコネクションを作成
            with self.GetSrvConnection(id, password) as conn:
            # with self.GetSrvConnectionWithSecure(id, password) as conn:
                # ユーザを検索し結果を取得（'sAMAccountName','homeDrive','homeDirectory'） Dict型に変換
                userinf = self.SrchLdapSrv(conn,id)[0].entry_attributes_as_dict
                # 事前にHome（H:）をアンマウント、削除しておく
                self.UnmountHomedrive()
                #（H:）をマウントする。
                self.MountHomedrive(userinf,id, password)
            logging.debug('AA')
        except Exception as exp:
            logging.exception(exp)
            print('Sorry Connection Exception System Exit')
            input('------Please Enter & Exit------')

if __name__ == "__main__":
    # ダブルクリックなどで実行された場合に”__name__”に”__name__”と入るのでここが実行される。
    logging.debug('VV')
    myClass=ConnectHomeDirectory()
    myClass.Main('','')
    logging.debug('AA')
    del myClass