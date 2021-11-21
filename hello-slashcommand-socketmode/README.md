# Hello Slack App with Socket Mode

This is an example Slack App using *Socket Mode*. The app establishes websocket connection without Bolt or Slack SDK, but with [websocket-client](https://github.com/websocket-client/websocket-client).

It is **not recommended** to go through full scratch to handle websocket events like this project. Use a flamework such as [Bolt](https://github.com/slackapi/bolt-python).

## 下準備

- Slack App を作成します
- Socket Mode を ON にします
- [こちらのページ](https://api.slack.com/interactivity/slash-commands)にしたがって, 新しく Slash Command を設定します
    - このとき command を `/hello` としてください
    > Socket Mode が ON になっていれば Slash Command が発火したときに Slack が POST するための Public な HTTP URL は要求されません(URL をセットすることと Socket Mode を ON にすることは排他であるため)．
    > もし要求された場合は Socket Mode が有効になっているか manifest を読むなどして確認してください．
- `connections.write` のスコープを持つ App-Level Token を発行しておきます

以上の手順を踏むと manifests は次のようになるでしょう(一部省略しています):
```yaml
_metadata:
  major_version: 1
  minor_version: 1
display_information:
  name: hello bot
features:
  bot_user:
    display_name: hello bot
    always_online: false
  slash_commands:
    - command: /hello
      description: 時間に合わせた挨拶を返します
      should_escape: false
oauth_config:
  scopes:
    bot:
      - commands
settings:
  socket_mode_enabled: true
```

manifests について詳しくは[公式リファレンス](https://api.slack.com/reference/manifests)を参照のこと．

## 実行方法

```sh
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
SLACK_APP_TOKEN=<xapp- prefixed App-Level Token> python hello.py
```

先ほど作成した Slack App をワークスペースにインストールし，適当なチャンネルもしくは DM で`/hello`と打ってみるとプログラムが返答します．

## 参考文献

- [Socket Mode implementation | Slack](https://api.slack.com/apis/connections/socket-implement)

- [Slack の Socket Mode API を使ってみた | KLab株式会社](https://www.klab.com/jp/blog/tech/2021/0201-slack.html)