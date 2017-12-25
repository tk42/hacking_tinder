# hacking_tinder
Auto sending likes on tinder

Tinder は外国初の出会い系アプリで，その手軽さ故に近年ユーザー数が伸びている

Facebook連動しており，Facebookユーザーでないと参加できない

気に入った女の子をLikeし，もしも向こうもLikeしたらマッチングして，メッセージのやりとりが可能になるというもの．

相手が非アクティブユーザーだと，なかなかマッチングすら叶わないので
結局男性の戦略としては「全員にLike」して，マッチしてからプロフィールを吟味したり，メッセージを練るという戦略で良いと思う．

iPhoneアプリではLikeは右スワイプになるが，これがなかなか面倒

そこで，自動でLikeを送り続けるようにするスクリプトを開発する

また，Face++のbeauty coreを利用して，美人スコアが高い人だけにライクを送る

https://www.faceplusplus.com/beauty/


Getting started
==========

1. rename setenv.sh.example and register your facebook token, face api key and face api secret key.

You can see how to get the facebook token [Tinderface](https://tinderface.herokuapp.com/) の導入をよく読む

After setting those,
```
. ./setenv.sh
```

2. enjoy!

```
./hacking_tinder.sh
```

### Trouble shooting
```
Some error was caught : 'ascii' codec can't encode characters in position 12-13: ordinal not in range(128)
```
みたいなのがでる場合，
```
echo $LANG
echo $LC_ALL
```
をチェックすること．だいたい次を設定すれば良い．
```
export LANG='ja_JP.UTF-8'
export LC_ALL='ja_JP.UTF-8'
```

To Small Bussiness
=====
[Tinderface](https://tinderface.herokuapp.com/)みたいなヤツ
