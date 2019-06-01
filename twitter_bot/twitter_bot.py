#!/usr/local/bin python3.7
# -*- coding: utf-8 -*-

# exe python3.7 twitter_bot.py

import os
import json
import logging

import twitter
import show_CO2_TEMP
import datetime


class Twitter_bot:
    '''twitter_bot autosend"tweet"\n
    "./twitter_token.json"にtwitterのToken情報を記載しておく必要があります．

    ---
    + twitter lib:https://pypi.org/project/twitter/

    '''
    # logfile
    logging.basicConfig(level=logging.DEBUG, filename='./Log.txt', filemode='w',
                        format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

    _jsondata = "./twitter_token.json"
    '''twitter tokenを記述しておく'''

    _fileimage = "./tmp.gif"
    '''Tweetに添付する画像ファイル名'''

    def loadJSON(self):
        '''JSONの読み取り class定数の”_jsondata”を読み取る
        '''
        logging.debug('VV')

        # Json読み取り
        return json.load(open(self._jsondata, 'r'))

    def setTokenMedia(self, obj_json):
        ''' 画像アップロード用
            読み込んだjsonからtwitter tokenの取り出しtwitterObjectをリターンする．
        '''
        logging.debug('VV')
        return twitter.Twitter(domain='upload.twitter.com', auth=twitter.OAuth(
            obj_json['token'], obj_json['token_secret'], obj_json['consumer_key'], obj_json['consumer_secret']))

    def setToken(self, obj_json):
        '''読み込んだjsonからtwitter tokenの取り出しtwitterObjectをリターンする．
        '''
        logging.debug('VV')

        return twitter.Twitter(auth=twitter.OAuth(
            obj_json['token'], obj_json['token_secret'], obj_json['consumer_key'], obj_json['consumer_secret']))

    def getSensorInf(self):
        '''センサーデータを取得'''
        logging.debug('VV')

        return show_CO2_TEMP.show_CO2_TEMP.get_Inf()

    def getFileImage(self):
        '''Tweetに添付する画像をカレントから取得する．
            事前にtmp.gifをカレントにおいておく必要がある．
        '''
        logging.debug('VV')
        with open(self._fileimage, "rb") as imagefile:
            img = imagefile.read()
        return img

    def uploadMedia(self, obj_twitter_media, img):
        '''画像をアップロードする．'''
        logging.debug('VV')

        return obj_twitter_media.media.upload(media=img)["media_id_string"]

    def updateTweet(self, obj_twitter, msg):
        '''ツイートする．'''
        logging.debug('VV')
        msg = datetime.datetime.now().isoformat()+"\n"+msg
        # Twitterに投稿
        rst = obj_twitter.statuses.update(status=msg)
        # logging.debug(rst)

        logging.debug('AA')

    def updateTweetWithImg(self, obj_twitter, msg, img):
        '''ツイートする．'''
        logging.debug('VV')

        # Twitterに投稿
        rst = obj_twitter.statuses.update(
            status=msg, media_ids=",".join([img]))
        # logging.debug(rst)

        logging.debug('AA')

    def genSendMsg(self, sesorinf):
        msg = ""
        msg = msg + datetime.datetime.now().isoformat()
        msg = msg + "\n"
        msg = msg + sesorinf

        return msg

    def main(self):
        '''メイン'''
        logging.debug('VV')

        obj_json = self.loadJSON(self)
        obj_twitter_media = self.setTokenMedia(self, obj_json)
        obj_twitter = self.setToken(self, obj_json)
        rsp_sensorinf = self.getSensorInf(self)
        fileimg = self.getFileImage(self)
        rsp_imgID = self.uploadMedia(self, obj_twitter_media, fileimg)
        logging.debug(rsp_imgID)

        sendmsg = self.genSendMsg(self, rsp_sensorinf)

        self.updateTweetWithImg(self, obj_twitter, sendmsg, rsp_imgID)

        logging.debug('AA')

    def __init__(self):
        ''''''


if __name__ == "__main__":
    # ダブルクリックなどで実行された場合に”__name__”に”__name__”と入るのでここが実行される
    logging.debug('VV')
    myclass = Twitter_bot
    myclass.main(myclass)
    logging.debug('AA')
