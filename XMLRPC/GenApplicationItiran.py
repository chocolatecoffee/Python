# -*- coding: utf-8 -*-
import logging
import json
import subprocess
import os
import sys
import platform
import socket
import Rpc_client

# ***事前準備***
# + PowerShellの文字コードを変える必要があります。PowerShellで 'chcp 65001' と実行して、文字コードをUTF-8に変更します。

# ログレベルのフォーマット Log.txtファイルに出力
logging.basicConfig(level=logging.DEBUG, filename='./Log.txt',
                    format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s', filemode='w')


class GenApplicationItiran:
    '''
        ダブルクリックをするとアプリケーション一覧のoutputJSON_管理名.jsonを作成します。\n
        実行される端末でPowerShellの実行が許可されていないと、IME,Storeアプリの一覧を取得できません。\n
    '''

    _stngs = {}
    '''読みだされた設定情報（Settings.json）を保管用'''

    _applicationitiran_json = {}
    '''アプリケーションの情報が記載されています。\n
    	例：\n
        "explorer": {\n
		"ViewName": "explorer",\n
		"Ver": "1.0.0",\n
		"Dir": "C://Windows//explorer.exe",\n
		"MD5": ["57fb57fc919229a8cf294ed8670c2d51","9fb049001a5aba2929d4fefcf53bec79"]\n
	},・・・\n
    ・ViewNameはアプリケーション一覧のアプリ名と一致している必要があります。アプリ一覧と比較し、同じならば・・・という処理を行うためです。\n
    '''

    # PowerShell IMEのリストを取得、ストアアプリのリストを取得
    _pshell_getIMELangSettingList = './getIMELangSettingList.ps1'
    _pshell_GetStoreApplication = './GetStoreApplication.ps1'

    # getmd5=getMD5.getMD5()
    # '''MD5算出をおこないます。'''

    def LoadJSON(self):
        '''[summary]
        サーバから指定されたJSONを読み取り、_setttings、_applicationitiran_jsonへ設定\n

        Returns:
            [type]: [description]
        '''

        try:
            client = Rpc_client.Rpc_client()
            jsons = client.RequestJSON()

            self._stngs = jsons.get('Settings.json')
            self._applicationitiran_json = jsons.get('ApplicationItiran.json')

            if self._stngs is None or self._applicationitiran_json is None:
                sys.exit('JSONが取得できない。')

        except Exception as exp:
            logging.exception(exp)
            sys.exit('LoadJSON-Error')

    def LoadPowerShell(self):
        '''[summary]
        サーバから指定されたPowerShellを読み取り、_setttings、_applicationitiran_jsonへ設定\n

        Returns:
            [type]: [description]
        '''

        pshell_getime = None
        pshell_getStore = None

        try:
            client = Rpc_client.Rpc_client()
            pshells = client.RequestPowerShell()

            pshell_getime = pshells.get(self._stngs['ps_cmd_01'])
            pshell_getStore = pshells.get(self._stngs['ps_cmd_02'])

            if pshell_getime is None or pshell_getStore is None:
                sys.exit('Powershellが取得できない。')

        except Exception as exp:
            logging.exception(exp)
            sys.exit('LoadPowerShell-Error')

        with open('./_'+self._stngs['ps_cmd_01'], mode='w', encoding=self._stngs['charcode_01']) as f:
            f.write(pshell_getime)

        with open('./_'+self._stngs['ps_cmd_02'], mode='w', encoding=self._stngs['charcode_01']) as f:
            f.write(pshell_getStore)

    def CheckOSSystem(self, outputJSON):
        '''
        OSのシステム部分　PC名の文字列からどこで運用されるシステムイメージかを判定し、"管理"に対す文字列をoutputJSONへ書き出す。\n
        アプリケーション一覧の"管理"の文字列と、該当する列番号を判定するものなので、同じにする必要がある。\n
        OS,実行されるPCが’Settings.json’と一致しない場合は、「設定情報が存在しません」を"管理"に設定する。\n
        また、ファイル名に「設定情報が存在しません」と入る。\n

        Arguments:\n
            outputJSON
        '''
        logging.debug('VV')

        pcname = platform.uname().node

        if self._stngs.get(pcname) is not None:
            outputJSON[self._stngs['kanri']
                       ] = self._stngs[pcname]
        else:
            logging.debug('実行したPC名がSettings.jsonに存在しません 実行PC名：' +
                          platform.uname().node)
            outputJSON[self._stngs['kanri']
                       ] = pcname + '_' + self._stngs['NoInfo']
            # outputJSON[self._stngs['kanri']] = pcname

        logging.debug('AA')

        return outputJSON

    def CheckApplication(self, outputJSON):
        '''読み込んだjsonFileDataをもとにインストールディレクトリにアプリがあるか確認する。\n
            MD5のチェックは行わないようにした。 20191101\n

            Arguments:
            jsonFileData [JSON Dict object]-- アプリの情報(MD5,インストールディレクトリ)が書かれたJSON\n
            outputJSON [JSON Dict object]-- アプリの有無の一覧・・・入力値の段階では"空"\n
            出力結果の例\n
            - outputJSONの出力・・・ApplicationItiran.jsonのViewNmae:'1'…ファイルが存在している\n
            - Logファイルへ出力・・・ApplicationItiran.jsonのkey名: Dir名 : NotFound…ファイルが存在していない。　ファイルがあるはずなのであれば、URLの記述ミスです。\n
        '''

        # アプリ一覧のJSOONデータをロード
        jsonFileData = self._applicationitiran_json

        for key in jsonFileData.keys():
            # logging.debug(key)
            #  "+Lhaca":{"ViewName":"+Lhaca","Ver": "1.5","Dir": "C://explorer.exe","MD5": "e4a81eddff8b844d85c8b45354e4144e"}

            for appdir in jsonFileData[key][self._stngs['Dir']]:

                # ファイルの存在の確認
                # 存在するのであれば、outputJSONへ"エクスプローラ": "1" と出力
                if os.path.exists(appdir):
                    outputJSON[jsonFileData[key]
                               [self._stngs['ViewName']]] = '1'

                    # MD5の確認を行う
                    # checkedMD5 = self.getmd5.checkMd5(appdir)
                    # if checkedMD5 in jsonFileData[key][self._stngs['Dir']]:
                    # logging.debug(jsonFileData[key][self._stngs['ViewName']] + ': checkedMD5 : ' + checkedMD5)
                    # outputJSON[jsonFileData[key][self._stngs['ViewName']]]='1'

                # 存在しないのであれば、Logファイルへ "エクスプローラ : C:\Windows\HelpPane_.exe : NotFound"と出力
                else:
                    logging.debug(key + ' : ' + appdir + ' : NotFound')

        return outputJSON

    def GetIMELangSetting(self, outputJSON):
        '''[利用ユーザのIMEに設定されている言語をoutputJSONへ追記する。]

        Arguments:
            outputJSON {[dict]} -- [アプリケーションインストール状況が乗ったデータ]

        Returns:
            [type] -- [IMEの設定情報を追加してリターン]
        '''

        # PowerShellを実行する。　実行する端末で、PowerShellの実行を許可していないと結果が出ません。
        # まずはPowerShellの文字コードをUTF-8に変更する。これをやらないとSJISで取得してしまい出力文字がおかしくなる。
        subprocess.run(self._stngs['ps_changecode'], shell=True)

        strScript = self._stngs['EXE_PowerShell'] + \
            ' ./_' + self._stngs['ps_cmd_01']

        logging.debug(strScript)

        # IMEに設定されている言語の一覧取得
        proc = subprocess.run(strScript, shell=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 取得した一覧をUTF-8に変換 結果が一行で出力されるので改行（\r\n）で区切る
        _ = proc.stdout.decode(
            self._stngs['charcode_01']).split('\r\n')

        # IME一覧の結果をJSONへ詰め込み
        for lang in _:
            outputJSON[lang] = '1'
            logging.debug(lang)

        return outputJSON

    def GetStoreApplication(self, outputJSON):
        '''[summary]

        Arguments:
            outputJSON {[type]} -- [description]

        Returns:
            [type] -- [description]
        '''

        subprocess.run(self._stngs['ps_changecode'], shell=True)

        strScript = self._stngs['EXE_PowerShell'] + \
            ' ./_' + self._stngs['ps_cmd_02']

        logging.debug(strScript)

        proc = subprocess.run(
            strScript, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _ = proc.stdout.decode(self._stngs['charcode_01']).split('\r\n')

        for App in _:
            outputJSON[App] = '1'
            logging.debug(App)

        return outputJSON

    def SendResultsServer(self, saveFile, outputJSON):
        '''[summary]

        Args:
            saveFile ([type]): [description]
            outputJSON ([type]): [description]
        '''

        client = Rpc_client.Rpc_client()
        client.SendMsg(saveFile, outputJSON)

    def main(self):
        '''メイン。全体的な流れのコントロールを行う。'''

        # logging.debug('VV')

        # #出力するJSONデータ 初期値　何もなし
        outputJSON = {}

        # 出力する結果ファイル
        saveFile = ''

        # 設定情報読み出し
        self.LoadJSON()

        # PowerShellファイルのロード、保管
        self.LoadPowerShell()

        # OSシステムを確認して、outputJSON へ'管理:???'の要素を追加する
        outputJSON = self.CheckOSSystem(outputJSON)

        # 読み込んだJSONをもとにインストールディレクトリにアプリがあるか確認、アプリの有無の一覧（JSONの形式{"explorer":"1","+Lhaca":"0"}）をリターン
        outputJSON = self.CheckApplication(outputJSON)

        # IMEに設定されている言語をoutputJSONへ追記する。
        outputJSON = self.GetIMELangSetting(outputJSON)

        # ストアアプリのアプリ名を追加
        outputJSON = self.GetStoreApplication(outputJSON)

        saveFile = self._stngs['saveFileName'].format(
            outputJSON[self._stngs['kanri']])

        self.SendResultsServer(saveFile, outputJSON)

        print('OutPut:' + saveFile)

        # JSONファイル形式で出力
        # json.dump(outputJSON,open('.//outputJSON.json','w', encoding="cp932"),ensure_ascii=False, indent=2)
        # json.dump(outputJSON, open(  saveFile, 'w', encoding = self._stngs['charcode_01']), ensure_ascii=False, indent=2)

        # 4. 出力されたファイルをGoogleDriveの所定の場所へコピぺ

        # 終了

        # logging.debug('AA')

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
    # ダブルクリックなどで実行された場合に”__name__”に”__name__”と入るのでここが実行される。
    logging.debug('VV')
    print('実行しています.')
    myClass = GenApplicationItiran()
    myClass.main()
    print('OutPut:Log_Client.txt,Log.txt. [Push ENTER]')
    input()
    del myClass
    logging.debug('AA')
