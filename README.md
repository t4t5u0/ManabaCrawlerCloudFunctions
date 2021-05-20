# ManabaCrawlerCloudFunctions
manaba の crawler を Cloud Functions で動かすやつ


## とりあえず試してみたい人
useridに学籍番号、passwordにパスワードを入力してください。
```bash
curl -X 'post' https://us-central1-question-bot-276707.cloudfunctions.net/manaba_unsubmitted/?userid=学籍番号&password=パスワード
```

utf-8 形式で出力されるので、いい感じに加工してください。一番簡単なのは末尾に `| jq` とつけることです。

## APIとして利用
他のAPIと同様にPOSTリクエストを受け付けます。節度ある利用をお願いします
