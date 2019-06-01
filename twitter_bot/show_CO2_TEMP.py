#!/usr/local/bin python3.7
# -*- coding: utf-8 -*-

from CO2Meter import *
from time import sleep


class show_CO2_TEMP:

    def get_Inf():
        # CO2meterが認識されているデバイスを設定
        # 他にUSBデバイス挿してると末尾が1とか2とかになってるかもしれません。
        sensor = CO2Meter("/dev/hidraw0")
        # ちょっと待つ
        sleep(10)
        # CO2濃度を取得(単位はppm)
        co2 = sensor.get_co2()
        temp = sensor.get_temperature()

        return "#CO2  {}ppm".format(co2["co2"]) + "\n" + "#TEMPERATURE  {}℃".format(temp["temperature"])

        # 表示
        # print("CO2: {}ppm".format(co2["co2"]))
        # print("TEMP: {}℃".format(temp["temperature"]))

    def __init__():
        ''''''


if __name__ == "__main__":
    # ダブルクリックなどで実行された場合に”__name__”に”__name__”と入るのでここが実行される。
    # logging.debug('VV')
    myclass = show_CO2_TEMP
    myclass.get_Inf()
    # logging.debug('AA')
