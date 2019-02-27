import logging
import json
import getMD5

# ログレベルのフォーマット Log.txtファイルに出力
logging.basicConfig(level=logging.DEBUG,filename='.\\Log.txt',format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

class genApplicationItiran:
    '''ダブルクリックをするとアプリケーション一覧の中間データを作成します。
    "ApplicationItiran.json"と一緒に扱います。
    '''

    # アプリケーション一覧の情報が書かれたJSONを指定。初期処理で場所を指定している　定数
    _jsondata=".\\ApplicationItiran.json"

    #MD5算出アプリ
    getmd5=getMD5.getMD5()

    #出力するJSONデータ
    outputJSON={'SYSTEMNAME':'中教室、だぇ・・・'}

    # 出力するディレクトリ・・・
    # PyDriveとgoogle-api-python-clientのインストールとGoogleへの申請が必要になります。oauthとかもいる。のでやらない。
    output_Dir= ''

    def load_JSON(self):
        '''JSONの読み取り ApplicationItiran.jsonを読み取る
        '''
        # logging.debug('VV')
        
        # Json読み取り
        jsonfileObj = open(self._jsondata,'r')
        jsonFileData = json.load(jsonfileObj)

        # logging.debug('AA')
        return jsonFileData

    def checkApplication(self,jsonFileData):
        
        '''読み込んだJSONをもとにインストールディレクトリにアプリがあるか確認
        Args:
            読み込んだJSONデータ
        Return:
            アプリの有無の一覧をリターン
        '''
        jsonFileDataKeys= jsonFileData.keys()
        jsonFileDataValues= jsonFileData.values()

        for key in jsonFileDataKeys:
        
            # logging.debug(key)
            # appinfo :
            # ライブラリ型・・・"+Lhaca":{"ViewName":"+Lhaca","Ver": "1.5","Dir": "C:\\explorer.exe","MD5": "e4a81eddff8b844d85c8b45354e4144e"}
            appinfo=jsonFileData[key]
            
            try:
                str_MD5=self.getmd5.checkMd5(appinfo['Dir'])
                # logging.debug(str_MD5)

                if str_MD5 == appinfo['MD5']:
                    # logging.debug(appinfo['MD5'])
                    # logging.debug('True')
                    # 有無をJSONの形式{"explorer":"1","+Lhaca":"0"}
                    self.outputJSON[appinfo['ViewName']]='1'
                    # logging.debug(self.outputJSON[appinfo['ViewName']])

                else:
                    # logging.debug(appinfo['MD5'])
                    # logging.debug('Flase')
                    # ファイルはあったがMD5が違う
                    # 有無をJSONの形式{"explorer":"1","+Lhaca":"0"}
                    self.outputJSON[appinfo['ViewName']]='0'
                    # logging.debug(self.outputJSON[appinfo['ViewName']])

            except FileNotFoundError:
                # logging.debug('FileNotFoundError')
                # ファイルが存在しない。
                # 有無をJSONの形式{"explorer":"1","+Lhaca":"0"}
                self.outputJSON[appinfo['ViewName']]='0'
                # logging.debug(self.outputJSON[appinfo['ViewName']])

        return self.outputJSON

    def __init__():
        logging.debug('VV')
        logging.debug('AA')

    def main(self):
        '''メイン。　実行される場所'''

        # logging.debug('VV')
        
        # 1. アプリの情報が書かれたJSONを読み込み
        jsonFileData =self.load_JSON(self)

        # 2. 読み込んだJSONをもとにインストールディレクトリにアプリがあるか確認、アプリの有無の一覧（JSONの形式{"explorer":"1","+Lhaca":"0"}）をリターン
        outputJSON = self.checkApplication(self,jsonFileData)

        # 3. JSONファイル形式で出力 出力先をデスクトップとかにしたい。
        json.dump(outputJSON,open('.\\outputJSON.json','w'),indent=4)

        # 4. 出力されたファイルをGoogleDriveの所定の場所へコピぺ

        # 終了
        
        # logging.debug('AA')

if __name__ == "__main__":
    # ダブルクリックなどで実行された場合に”__name__”に”__name__”と入るのでここが実行される。
    logging.debug('VV')
    myClass=genApplicationItiran
    myClass.main(myClass)
    logging.debug('AA')