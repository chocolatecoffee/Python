# Python
## Common
### [getMD5.py](https://github.com/chocolatecoffee/Python/blob/master/Common/getMD5.py)
+ calc MD5

## twitter_bot
### [twitter_bot.py](https://github.com/chocolatecoffee/Python/blob/master/twitter_bot/twitter_bot.py)
センサーデータをツイートする．  
センサーは[カスタム (CUSTOM) CO2モニター CO2-mini](https://www.amazon.co.jp/gp/product/B00I3XJ9LM/)  
取得したセンサーデータは「LoadAndAddJSON」でJSONへ記録する．

## LoadAndAddJSON
### [LoadAndAddJSON.py](https://github.com/chocolatecoffee/Python/blob/master/LoadAndAddJSON/LoadAndAddJSON.py)  
 twitter_botから渡されるセンサーデータを年ごとのファイルに月別，時間別でJSONに追記する．

## matplotlib
### 
LoadAndAddJSONで作成されたセンサーデータファイルからグラフを作成する．