# tap-jquants

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:

- Pulls raw data from [J-Quants](https://jpx-jquants.com/)
- Extracts the following resources:
  - [listed_info](https://jpx.gitbook.io/j-quants-ja/api-reference/listed_info)
  - [daily_quotes](https://jpx.gitbook.io/j-quants-ja/api-reference/daily_quotes)
  - [trades_spec](https://jpx.gitbook.io/j-quants-ja/api-reference/trades_spec)
  - [topix](https://jpx.gitbook.io/j-quants-ja/api-reference/topix)
- Outputs the schema for each resource
- Incrementally pulls data based on the input state

## 認証

[J-Quants API](https://jpx-jquants.com/) に登録したメールアドレスとパスワードが必要です。

## 使い方

### 1. インストール

このリポジトリーをcloneし、setup.pyを用いてインストールします。
Pythonの仮想環境を用いることが推奨されます。

> 以下、Python 3.9で動作確認しています。

```shell
> git clone git@github.com:stn/tap-jquants.git
> cd tap-jquants
> python3 -m venv venv
> source venv/bin/activate
> pip install .
```

### 2. 必要ライブラリー

ここでは、検証のため以下のライブラリーも用います。

```shell
> pip install target-csv
> pip install singer-tools
```

### 3. tapの設定

J-Quantsに登録したアカウントを用いて、以下のようなファイルを作成してください。
`start_date` 直近の営業日あるいは1営業日前を指定するといいでしょう
（[データの更新頻度・更新タイミング](https://jpx.gitbook.io/j-quants-ja/outline/data-update)）。
ファイル名は任意ですが、ここでは `config.json` とします。

```json
{
  "mail_address": "my_mail_address",
  "password": "my_password",
  "start_date": "YYYY-MM-DD"
}
```

### 4. Discovery

tapを[discoveryモード](https://github.com/singer-io/getting-started/blob/master/docs/DISCOVERY_MODE.md#discovery-mode)で実行し、catalog.jsonを作成します。

```shell
> venv/bin/tap-jquants --config config.json --discover > catalog.json
```

### 5. 実行（認証のみ）

出力された `catalog.json` を用いて、syncモードで実行します。

```shell
> venv/bin/tap-jquants --config config.json --catalog catalog.json
time=2023-04-17 11:12:50 name=singer level=INFO message=Get a refresh token, token expires = 2023-04-24 02:12:50.066456+00:00
time=2023-04-17 11:12:52 name=singer level=INFO message=Get the id token, token expires = 2023-04-18 02:12:52.456143+00:00
time=2023-04-17 11:12:52 name=singer level=INFO message=Skipping stream: daily_quotes
time=2023-04-17 11:12:52 name=singer level=INFO message=Skipping stream: indices_topix
time=2023-04-17 11:12:52 name=singer level=INFO message=Skipping stream: listed_info
time=2023-04-17 11:12:52 name=singer level=INFO message=Skipping stream: trades_spec
{"type": "STATE", "value": {"currently_syncing": null}}
```

J-Quantsへの認証が成功することを確認してください。

この実行では、すべてのstreamがスキップされています。

### 6. Sync

`catalog.json` をエディターで開き、読み込みたいstreamのschema定義に次のように `"selected": true,` を挿入します。

```json
...
      "tap_stream_id": "daily_quotes",
        "schema": {
           "selected": true,
           "properties": {
...
```

ここでは`tap-jquants`の結果をCSVで書き出すことにします。

```shell
> venv/bin/tap-jquants --config config.json --catalog catalog.json | venv/bin/target-csv
```

結果は`daily_quotes-YYYYMMDDThhmmss.csv`というファイルに出力されます。

### 7. 次のステップ

ここでは、`tap-jquants` の動作確認を説明しました。

[Singer](https://singer.io) tapとしてJ-Quants APIを利用可能にする `tap-jquants` を用いることで、
コードを書くことなくJSONファイルによる設定だけでデータを取得できるようになりました。

ここでは説明しませんでしたが、tapが最後に出力している
`{"currently_syncing": null, "bookmarks": {"daily_quotes": "2023-04-14"}}`
という行を `state.json` などに保存し、`--state state.json` と指定することで、
インクリメンタルなアップデートが可能となります。

また、[meltano](https://meltano.com/) を利用することで、
これらの設定と実行はより簡単になります。


## 開発者向け

`singer-check-tap` をtargetに指定することで詳細な情報を得ることができます。

```shell
❯ tap-jquants --config config.json --catalog catalog.json| singer-check-tap 
Checking stdin for valid Singer-formatted data
INFO Get a refresh token, token expires = 2023-04-24 02:57:47.781546+00:00
INFO Get the id token, token expires = 2023-04-18 02:57:50.130585+00:00
INFO Starting sync for stream: daily_quotes
INFO Starting Sync for Stream daily_quotes
INFO bookmark value or start date for daily_quotes: 2023-04-14 00:00:00+00:00
INFO Running sync for daily_quotes between date window 2023-04-14 2023-04-15
INFO params = {'date': '2023-04-14'}, payload = {}
INFO METRIC: {"type": "timer", "metric": "http_request_duration", "value": 3.6500508785247803, "tags": {"endpoint": "daily_quotes", "http_status_code": 200, "status": "succeeded"}}
INFO Total synced records for daily_quotes: 4261
INFO Stream: daily_quotes, Processed 4261 records
INFO METRIC: {"type": "counter", "metric": "record_count", "value": 4261, "tags": {"endpoint": "daily_quotes"}}
INFO Write state for Stream: daily_quotes, value: 2023-04-14
INFO Running sync for daily_quotes between date window 2023-04-15 2023-04-16
INFO params = {'date': '2023-04-15'}, payload = {}
INFO METRIC: {"type": "timer", "metric": "http_request_duration", "value": 0.20042181015014648, "tags": {"endpoint": "daily_quotes", "http_status_code": 200, "status": "succeeded"}}
INFO Write state for Stream: daily_quotes, value: 2023-04-14
INFO Running sync for daily_quotes between date window 2023-04-16 2023-04-17
INFO params = {'date': '2023-04-16'}, payload = {}
INFO METRIC: {"type": "timer", "metric": "http_request_duration", "value": 0.20950675010681152, "tags": {"endpoint": "daily_quotes", "http_status_code": 200, "status": "succeeded"}}
INFO Write state for Stream: daily_quotes, value: 2023-04-14
INFO Running sync for daily_quotes between date window 2023-04-17 2023-04-17
INFO params = {'date': '2023-04-17'}, payload = {}
INFO METRIC: {"type": "timer", "metric": "http_request_duration", "value": 0.22565102577209473, "tags": {"endpoint": "daily_quotes", "http_status_code": 200, "status": "succeeded"}}
INFO Write state for Stream: daily_quotes, value: 2023-04-14
INFO Total records extracted for Stream: daily_quotes: 4261
INFO Finished Sync for Stream daily_quotes
INFO Skipping stream: indices_topix
INFO Skipping stream: listed_info
INFO Skipping stream: trades_spec
The output is valid.
It contained 4268 messages for 1 streams.

      1 schema messages
   4261 record messages
      6 state messages

Details by stream:
+--------------+---------+---------+
| stream       | records | schemas |
+--------------+---------+---------+
| daily_quotes | 4261    | 1       |
+--------------+---------+---------+
```


## Credits

- [J-Quants](https://jpx-jquants.com/)
- [Singer](https://singer.io)
- [singer-tap-template](https://github.com/singer-io/singer-tap-template)
  - The initial `tap-jquants` code is generated by the `singer-tap-template`.
- [tap-google-search-console](https://github.com/singer-io/tap-google-search-console)
  - A part of `tap-jquants` code is based on and modified from `tap-google-search-console`.

---

Copyright &copy; 2023 Akira Ishino
