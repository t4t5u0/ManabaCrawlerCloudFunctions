# ManabaCrawlerCloudFunctions
manaba の crawler を Cloud Functions で動かすやつ


## とりあえず試してみたい人
useridに学籍番号、passwordにパスワードを入力してください。
```bash
curl -X 'post' 'https://us-central1-question-bot-276707.cloudfunctions.net/manaba_unsubmitted/?userid=学籍番号&password=パスワード'
```

utf-8 形式で出力されるので、いい感じに加工してください。一番簡単なのは末尾に `| jq` とつけることです。

## APIとして利用
他のAPIと同様にPOSTリクエストを受け付けます。節度ある利用をお願いします。

返り値は
```json
[
  {
    "course_id": 95655,
    "course_name": "技術者倫理 3",
    "description": "",
    "end": "2021-05-25 00:00",
    "remain": "4 days, 9:29:17.815893",
    "start": "2021-05-18 13:40",
    "state": "未提出",
    "task_id": 101403,
    "task_title": "第6回ミニエッセイ課題",
    "task_url": "https://manaba.fun.ac.jp/ct/course_95655_query_101403"
  }
]
```
のような形です
