#!/usr/local/bin python3.7
# -*- coding: utf-8 -*-

# exe python3.7 twitter_bot.py

import json
import logging
import twitter

class Twitter_bot:
    '''twitter_bot autosend'tweet'\n
    './twitter_token.json'にtwitterのToken情報を記載しておく必要があります．

    ---
    + twitter lib:https://pypi.org/project/twitter/

    '''
    
    # logfile
    logging.basicConfig(level=logging.DEBUG, filename='./Log.txt', filemode='w',format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

    _jsondata = './twitter_token.json'
    '''twitter tokenを記述しておく'''

    def _LoadJSON(self):
        '''JSONの読み取り ”_jsondata”を読み取る
        '''
        logging.debug('VV')

        # Json読み取り
        return json.load(open(self._jsondata, 'r'))
    
    def UpdateTweet(self, msg):
        '''[通常のTweet]
        
        Args:
            msg ([str]): [tweetmessage]
        '''
        logging.debug('VV')
        self.UpdateTweetWithImg(self,msg,None)
        logging.debug('AA')

    def UpdateTweetWithImg(self, msg, img):
        '''[画像付でツイートする．]
        
        Args:
            msg ([str]): [tweetmessage]
            img ([str]): [image path]
        '''        

        logging.debug('VV')

        obj_json = self._LoadJSON(self)

        obj_twitter = twitter.Twitter(auth=twitter.OAuth(obj_json['token'], obj_json['token_secret'], obj_json['consumer_key'], obj_json['consumer_secret']))
        
        if img != None:
            # 画像ファイルのパラメータがある場合 画像付ｓでTweet
            obj_twitter_media = twitter.Twitter(domain='upload.twitter.com', auth=twitter.OAuth(obj_json['token'], obj_json['token_secret'], obj_json['consumer_key'], obj_json['consumer_secret']))

            with open(img, 'rb') as imagefile:
                uploard_img = imagefile.read()

            img_id = obj_twitter_media.media.upload(media=uploard_img)['media_id_string']

            # Twitterに投稿
            rst = obj_twitter.statuses.update(status=msg, media_ids=','.join([img_id]))

        else:
            # 画像ファイルのパラメータがない場合 通常のTweet
            # Twitterに投稿
            rst = obj_twitter.statuses.update(status=msg)

        logging.debug(rst)
        logging.debug('AA')

    def main(self):
        '''[メイン 何も実行しない．デバッグ用．]
        '''        

        logging.debug('VV')
        #self.UpdateTweetWithImg(self,'testmsg','./testimg.gif')
        #self.UpdateTweet(self,'Noimage testmsg')
        logging.debug('AA')

    def __init__(self):
        ''''''

if __name__ == '__main__':
    # ダブルクリックなどで実行された場合に”__name__”に”__name__”と入るのでここが実行される
    logging.debug('VV')
    myclass = Twitter_bot
    myclass.main(myclass)
    logging.debug('AA')
