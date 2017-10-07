# hacking_tinder
Auto sending likes on tinder

Tinder は外国初の出会い系アプリで，その手軽さ故に近年ユーザー数が伸びている

Facebook連動しており，Facebookユーザーでないと参加できない

気に入った女の子をLikeし，もしも向こうもLikeしたらマッチングして，メッセージのやりとりが可能になるというもの．

相手が非アクティブユーザーだと，なかなかマッチングすら叶わないので
結局男性の戦略としては「全員にLike」して，マッチしてからプロフィールを吟味したり，メッセージを練るという戦略で良いと思う．

iPhoneアプリではLikeは右スワイプになるが，これがなかなか面倒

そこでWeb版Tinder https://tinder.com/ をハックして，自動でLikeを送り続けるようにするスクリプトを開発する


-------

HttpRequestを解析した結果，Facebook認証後に api.gotinder.com のAPIにGETリクエストを投げればLikeが送れることがわかった．

0. X-Auth-Token を取得する
パケットキャプチャなどして，https://api.gotinder.com/v2/profile に向かうGETリクエストヘッダを覗き見て x-auth-token を取得しておく
```
python hacking_tinder.py (x-auth-token)
```

1. 女の子のダウンロード
下記APIを叩けば，女の子は11人まとめてバッチでダウンロードされる
```
https://api.gotinder.com/recs/core?locale=ja
```

これにより下記のJSON Responceを得る
```
{"status":200,"results":[
{"type":"user","group_matched":false,"user":
 _id:
 name:
 bio:
 birth_date:
 distance_mi:
 photos:[]
 ...
},
{"type":"user","group_matched":false,"user":
 ...
},
]
```
つまり，送るべきユーザIDは
```
results.0.user._id
results.1.user._id
...
results.10.user._id
```
となる．

長いJSONレスポンスには色々と面白いものもあるので，是非他のものにも活用したい．

Online JSON viewer http://jsonviewer.stack.hu/

2. 女の子にLikeを送る
```
https://api.gotinder.com/like/(_id)?locale=ja
```
に対してGETリクエストを繰り返せば良い．

課題
- [ ] X-Auth-Token のキャプチャをユーザフレンドリーに行う
