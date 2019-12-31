# Python
## [Common](https://github.com/chocolatecoffee/Python/tree/master/Common)
### [getMD5.py](https://github.com/chocolatecoffee/Python/blob/master/Common/getMD5.py)
+ calc MD5

## [twitter_bot](https://github.com/chocolatecoffee/Python/tree/master/twitter_bot)
### [twitter_bot.py](https://github.com/chocolatecoffee/Python/blob/master/twitter_bot/twitter_bot.py)
+ [センサーのデータを取得するプログラム:CO2Meter](https://github.com/heinemml/CO2Meter)を利用．

+ センサーデータをツイートする．  
センサーは[カスタム (CUSTOM) CO2モニター CO2-mini](https://www.amazon.co.jp/gp/product/B00I3XJ9LM/)を利用．  
取得したセンサーデータは「LoadAndAddJSON」でJSONへ記録する．  

### [GrafGenerater.py](https://github.com/chocolatecoffee/Python/blob/master/twitter_bot/GrafGenerater.py)

+ LoadAndAddJSONで作成したファイル（20XX_SensorData.json）から昨日，月別，年別でグラフを作成する．  
年始に一年分，月初めに一ヶ月分，日が変わる頃に昨日のデータを抽出し，それぞれ年別，月別，昨日分のグラフを作成する．

  + *generate CO2 Graph*  
  + *Testing generate Temp Graph*

## [LoadAndAddJSON](https://github.com/chocolatecoffee/Python/tree/master/LoadAndAddJSON)
### [LoadAndAddJSON.py](https://github.com/chocolatecoffee/Python/blob/master/LoadAndAddJSON/LoadAndAddJSON.py)  

*in the "twitter_bot"*
+ twitter_botから渡されるセンサーデータを年ごとのファイル（20XX_SensorData.json）に月別，時間別でJSONに追記する．

