# Python
## [Common](https://github.com/chocolatecoffee/Python/tree/master/Common)
### [getMD5.py](https://github.com/chocolatecoffee/Python/blob/master/Common/getMD5.py)
+ calc MD5

## [twitter_bot](https://github.com/chocolatecoffee/Python/tree/master/twitter_bot)
+ [センサーのデータを取得するプログラム:CO2Meter](https://github.com/heinemml/CO2Meter)をカスタムして利用．
+ [センサーのデータを取得するプログラム:SensorBME280](https://github.com/SWITCHSCIENCE/samplecodes/tree/master/BME280)をカスタムして利用．

### [twitter_bot.py](https://github.com/chocolatecoffee/Python/blob/master/twitter_bot/twitter_bot.py)
+ Tweetするプログラム
  + UpdateTweet・・・文字列だけでTweet．
  + UpdateTweetWithImg・・・文字列＋画像付でTweet．

### [CtrlTwitter.py](https://github.com/chocolatecoffee/Python/tree/master/twitter_bot/CtrlTwitter.py)

+ センサーデータを取得して，Tweetする．
+ 取得したセンサーデータは「LoadAndAddJSON」でJSONへ記録する．

### [LoadAndAddJSON.py](https://github.com/chocolatecoffee/Python/blob/master/twitter_bot/LoadAndAddJSON.py)  
+ CtrlTwitterから渡されるセンサーデータを年ごとのファイル（20XX_SensorData.json）に月別，日別，各センサーデータ別(CO2,Temp,Barometer,Humidity)でJSONに追記する．

### [GraphGenerater.py](https://github.com/chocolatecoffee/Python/blob/master/twitter_bot/GraphGenerater.py)

+ LoadAndAddJSONで作成したファイル（20XX_SensorData.json）から昨日，月別，年別でグラフを作成する．  
年始に一年分，月初めに一ヶ月分，日が変わる頃に昨日のデータを抽出し，それぞれ年別，月別，昨日分のグラフを作成する．

  + generate CO2 Graph
    + *Testing generate Colorbar,XLabel,YLabel*
  + *Testing generate Temp, Barometer,Humidity Graph*
