import os
import json
import logging

import twitter


class Twitter_bot:
    '''twitter_bot autosend"tweet"
    ".\\twitter_token.json"にtwitterのToken情報を記載しておく必要があります．

    ---
    + twitter lib:https://pypi.org/project/twitter/

    '''
    # logfile
    logging.basicConfig(level=logging.DEBUG, filename='.\\Log.txt',
                        format=' %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

    # twitter tokenを記述しておく
    _jsondata = ".\\twitter_token.json"

    def load_JSON(self):
        '''JSONの読み取り class定数の”_jsondata”を読み取る
        '''

        # Json読み取り
        return json.load(open(self._jsondata, 'r'))

    def set_token(self, obj_json):
        '''読み込んだjsonからtwitter tokenの取り出しtwitterObjectをリターンする．
        '''

        return twitter.Twitter(auth=twitter.OAuth(
            obj_json['token'], obj_json['token_secret'], obj_json['consumer_key'], obj_json['consumer_secret']))

    def update_tweet(self, obj_twitter):
        '''ツイートする'''

        # 投稿メッセージ
        msg = "TEST_MSG"

        # Twitterに投稿
        rst = obj_twitter.statuses.update(status=msg)
        logging.debug(rst)

    def main(self):
        '''メイン'''

        obj_json = self.load_JSON(self)
        obj_twitter = self.set_token(self, obj_json)
        self.update_tweet(self, obj_twitter)

    def __init__(self):
        ''''''


if __name__ == "__main__":
    # ダブルクリックなどで実行された場合に”__name__”に”__name__”と入るのでここが実行される。
    logging.debug('VV')
    myclass = Twitter_bot
    myclass.main(myclass)
    logging.debug('AA')
