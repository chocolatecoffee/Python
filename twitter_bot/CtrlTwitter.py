#!/usr/local/bin python3.7
# -*- coding: utf-8 -*-

import logging
import datetime
import CO2Meter
import LoadAndAddJSON
import twitter_bot
import SensorBME280
import time

class CtrlTwitter:

    # ログレベルのフォーマット Log.txtファイルに出力
    logging.basicConfig(level=logging.DEBUG, filename='./Log.txt', filemode='w', format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

    def GenSendMsg(self, co2, temp, pressure, hum, rsp_sensor1_temp):
        '''[Tweetメッセージを作成．CO2濃度と気温を書き込みメッセージに入れる．]
        
        Args:
            co2 (float): CO2濃度
            temp (float): 気温
            pressure (float): 気圧
            hum (float): 湿度
            sensor1_temp (float): 気温
        
        Returns:
            [str]: [Tweetメッセージ]
        '''        

        msg = ''
        msg = msg + datetime.datetime.now().isoformat()+ '\n'
        msg = msg + '\n' + '--- CO2Meter ---'+'\n'
        msg = msg + '#CO2 {}ppm'.format(co2)+'\n'
        msg = msg + '#TEMPERATURE {}℃'.format(temp)+'\n'
        msg = msg + '#TEMPERATURE {}℉'.format(round((temp * 1.8) + 32.0, 1)) + '\n'
        msg = msg + '\n' + '--- HiLetgo BME280 ---' + '\n'
        msg = msg + '#PRESSURE {}hpa'.format(pressure) + '\n'
        msg = msg + '#HUMIDITY {}%'.format(hum) + '\n'
        msg = msg + '#TEMPERATURE {}℃'.format(rsp_sensor1_temp) + '\n'

        return msg

    def UpdateTweetMsg(self, msg):
        '''[Twitter_botでTweet]
        
        Args:
            sendmsg ([str]): [Tweetメッセージ]
        '''        
        _ = twitter_bot.Twitter_bot()
        _.UpdateTweet(msg)

    def WriteSensordataToJSON(self, temp, co2, pressure, hum):
        '''[センサーデータを記録]
        
        Args:
            temp (float): 気温
            co2 (float): CO2濃度
            pressure (float): 気圧
            hum (float): 湿度
        '''        
        
        sensordata = {'Temp': str(temp), 'CO2': str(co2), 'Barometer': str(pressure), 'Humidity': str(hum)}
        # {'Temp': '22.5', 'CO2': '450', 'Barometer': '1013', 'Humidity': '40'}

        _ = LoadAndAddJSON.LoadAndAddJSON()
        _.add_SensorDataToJSON(sensordata)
        
    def main(self):
        '''
            センサーデータの取得 ～ Tweet ～ センサーデータの記録を行うメインメソッド．
            Sensor：CO2Meter,BME280
        '''        
        logging.debug('VV')

        # SensorBME280センサーへアクセス・データの取得
        sensor1 = SensorBME280.bme280()
        rsp_sensor1_pressure, rsp_sensor1_hum, rsp_sensor1_temp = sensor1.Main()

        # CO2センサーへアクセス・データの取得
        sensor0 = CO2Meter.CO2Meter('/dev/hidraw0')
        # ちょっと待つ
        time.sleep(10)
        rsp_sensor0_co2, rsp_sensor0_temp = sensor0.get_data()

        # Tweetメッセージの生成
        sendmsg = self.GenSendMsg(rsp_sensor0_co2['co2'], rsp_sensor0_temp['temperature'], rsp_sensor1_pressure, rsp_sensor1_hum, rsp_sensor1_temp)

        # センセーのデータをTweet
        self.UpdateTweetMsg(sendmsg)

        #センサーデータを記録
        self.WriteSensordataToJSON(rsp_sensor0_temp['temperature'], rsp_sensor0_co2['co2'], rsp_sensor1_pressure, rsp_sensor1_hum)

        logging.debug('AA')

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

if __name__ == '__main__':
    # ダブルクリックなどで実行された場合に”__name__”に”__name__”と入るのでここが実行される
    logging.debug('VV')
    myclass = CtrlTwitter()
    myclass.main()
    del myclass
    logging.debug('AA')