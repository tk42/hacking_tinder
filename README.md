# hacking_tinder
Auto sending likes on tinder

Tinder は外国初の出会い系アプリで，その手軽さ故に近年ユーザー数が伸びている

Facebook連動しており，Facebookユーザーでないと参加できない

気に入った女の子をLikeし，もしも向こうもLikeしたらマッチングして，メッセージのやりとりが可能になるというもの．

相手が非アクティブユーザーだと，なかなかマッチングすら叶わないので
結局男性の戦略としては「全員にLike」して，マッチしてからプロフィールを吟味したり，メッセージを練るという戦略で良いと思う．

iPhoneアプリではLikeは右スワイプになるが，これがなかなか面倒

そこで，自動でLikeを送り続けるようにするスクリプトを開発する

また，Face++のbeauty scoreを利用して，[美人スコア](https://www.faceplusplus.com/beauty/)(定義のページが削除されている…)が高い人だけにライクを送る


Getting started
==========

1. register your facebook email, facebook password, face api key and face api secret key, and then rename setenv.sh.example to setenv.sh.

2. install
```
make build
```

3. enjoy!
```
make run
```

4. run tests for developpers
```
make test
```

### Trouble shooting
If you see the following error;
```
Some error was caught : 'ascii' codec can't encode characters in position 12-13: ordinal not in range(128)
```
, you should check $LANG and $LC_ALL.
```
echo $LANG
echo $LC_ALL
```
As you use Japanese emojis, you should set those as follows;
```
export LANG='ja_JP.UTF-8'
export LC_ALL='ja_JP.UTF-8'
```

Future work
=====
Beyond [Tinderface](https://tinderface.herokuapp.com/)
