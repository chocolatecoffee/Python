import logging
import json
import datetime
from collections import OrderedDict
import os

# ログレベルのフォーマット Log.txtファイルに出力
logging.basicConfig(level=logging.DEBUG, filename='./Log.txt', filemode='w',format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

class LoadAndAddJSON:
    '''センサーのデータを_jsonfileへ月別に毎日毎時のデータを追記するクラス
    '''
    
    _today = datetime.datetime.now()
    '''datetime obj "Today"
    '''
    # _today = datetime.datetime.now().isoformat()
    # today 2019-10-17T23:11:56.338690

    _jsonfile = './{}_SensorData.json'.format(_today.year)
    '''年ごとにjsonファイルを作成 "2019_SensorData.json"と先頭に年が入る
    '''
    
    _Newjson_format = {}
    '''新規作成用のJSON「空」フォーマット
    '''

    ''' 出力されるJSONデータの形式を変更したためコメントアウト 20200101'''
    #def add_SensorDataToJSON(self ,sensordata):
    #    '''Args(センサーのデータ)を_jsonfileへ追記する．月別に毎日毎時のデータを追記する．\n
    #    _jsonfileの形式：\n
    #    {"01": [{"dd": "01","H": "01","mm": "00","Temp": "22.5","CO2": "450","Barometer": "1013","Humidity": "40"},・・・]}\n
    #   対応する内容\n
    #    {"月": [{"日": "01","時": "01","分": "00","Temp": "22.5","CO2": "450","Barometer": "1013","Humidity": "40"},・・・]}\n
    #    
    #    Args:
    #        sensordata ([Dict]):class twitter_botから送られたセンサーのデータ\n
    #        例):{"Temp": "22.5", "CO2": "450", "Barometer": "1013", "Humidity": "40"}
    #
    #    Returns:no return
    #    '''
    #
    #    logging.debug('VV')
    #
    #    # print(today.year, "年", today.month, "月", today.day, "日", today.hour,"時", today.minute, "分", today.second, "秒", today.microsecond, "マイクロ秒")
    #
    #    # json 階層の確認 月の階層があるかの判定 新規の場合に　_today.monthで階層を作成する。
    #    
    #    # "01": [{ "dd": "01","H": "01","mm": "00","Temp": "22.5","CO2": "450","Barometer": "1013","Humidity": "40"},
    #    add_info ={"dd": str(self._today.day), "HH": str(self._today.hour), "mm":str(self._today.minute),"Temp":sensordata["Temp"],"CO2":sensordata["CO2"],"Barometer":sensordata["Barometer"],"Humidity":sensordata["Humidity"]}
    #    
    #    jsonobj=self._load_JSON(self,self._jsonfile)
    #
    #    if str(self._today.month) in jsonobj.keys():
    #        jsonobj[str(self._today.month)].append(add_info)
    #
    #    else:
    #        jsonobj.setdefault(str(self._today.month), [])
    #        jsonobj[str(self._today.month)].append(add_info)
    #        
    #    json.dump(jsonobj, open(self._jsonfile, 'w'), indent=4)
    #
    #    logging.debug('AA')

    def add_SensorDataToJSON(self, sensordata):
        '''[sensordataを_jsonfileへ追記する．月別，日別，CO2濃度別，気温別，気圧別，湿度別にデータを追記する．

        _jsonfileの形式：

        {
            "1": {
                ”1”:{
                    "CO2":["450",・・・],
                    "Temp":["22.5",・・・],
                    "Barometer":["1013",・・・],
                    "Humidity":["40",・・・],
                    },
                "2":{・・・},
                ・・・
        }

        対応する内容
        {"月": ["日": ["CO2":["sensordataのCO2",・・・],"Temp":["sensordataの気温",・・・],"Barometer":["sensordataの気圧",・・・],"Humidity":["sensordataの湿度",・・・]]]
        
        Args:
            sensordata ([Dict]): [class twitter_botから送られたセンサーのデータ
            例):{"Temp": "22.5", "CO2": "450", "Barometer": "1013", "Humidity": "40"}]

        Returns:no return. output _jsonfile
        '''

        logging.debug('VV')

        mo = str(self._today.month)
        # mo = "1"

        today = str(self._today.day)
        #today = "1"

        # json 階層の確認 月の階層があるかの判定 新規の場合に　_today.monthで階層を作成する。
        jsonobj = self._load_JSON(self, self._jsonfile)
        
        # json内に今月の文字列が存在する．
        if mo in jsonobj.keys():
            
            #json内に今日の日にちの文字列が存在しない．
            if not today in jsonobj[mo].keys():
                ''' '''
                jsonobj[mo].setdefault(today, {})
                jsonobj[mo][today].setdefault("CO2", [])
                jsonobj[mo][today].setdefault("Temp", [])
                jsonobj[mo][today].setdefault("Barometer", [])
                jsonobj[mo][today].setdefault("Humidity", [])

            else:
                ''' '''
        else:
            ''' '''
            jsonobj.setdefault(mo, {}).setdefault(today, {})
            jsonobj[mo][today].setdefault("CO2", [])
            jsonobj[mo][today].setdefault("Temp", [])
            jsonobj[mo][today].setdefault("Barometer", [])
            jsonobj[mo][today].setdefault("Humidity", [])
        
        jsonobj[mo][today]["CO2"].append(sensordata["CO2"])
        jsonobj[mo][today]["Temp"].append(sensordata["Temp"])
        jsonobj[mo][today]["Barometer"].append(sensordata["Barometer"])
        jsonobj[mo][today]["Humidity"].append(sensordata["Humidity"])

        json.dump(jsonobj, open(self._jsonfile, 'w'), indent=4)

        logging.debug('AA')

    def _load_JSON(self,jsonfile):
        '''_jsonfileをロードしReturnする．存在しなければ，空のフォーマット「_Newjson_format」で新規作成しReturnをする．

        Args:
            _jsonfile ([Dict]): 年ごとにjsonファイル

        Returns:
            読み出したjsonfile [Dict]: [年ごとにjsonファイル]
        '''

        logging.debug('VV')

        if (os.path.exists(jsonfile)):
            '''ここではファルの存在確認だけ．処理なし．'''

        else:
            # with open(jsonfile, 'w') as f:
            #    f.write("")
            #logging.debug(jsonfile)
            json.dump(self._Newjson_format, open(jsonfile, 'w'), indent=4)

        logging.debug('AA')

        return json.load(open(jsonfile, 'r'))

    def main(self):
        '''ダブルクリックなどで実行された場合にmainを実行
        '''

        Test_sensordata = {"Temp": "22.5", "CO2": "400", "Barometer": "1013", "Humidity": "40"}

        logging.debug('VV')

        self.add_SensorDataToJSON(self, Test_sensordata)
        
        logging.debug('AA')

    def __init__(self):
        '''
        '''
        logging.debug('VV')
        logging.debug('AA')

if __name__ == "__main__":
    # ダブルクリックなどで実行された場合に”__name__”に”__name__”と入るのでここが実行される。
    logging.debug('VV')
    myClass = LoadAndAddJSON
    myClass.main(myClass)
    logging.debug('AA')
