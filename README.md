# APEX Legends 戦績表示 Discord BOT

このプロジェクトは、**Apex Legends の戦績情報を Discord 上で表示・分析する BOT** です。  
ユーザーはスラッシュコマンド（例：`/apex`）を使用して、Origin / PSN / XBL のいずれかのプラットフォームでプレイヤー名を指定し、最新の戦績や戦績の差分、グラフによる視覚的分析を確認できます。

## 主な機能

- 任意プレイヤーの戦績取得（TRN API またはダミーデータ）
- キル/マッチ（K/M）比の推移をグラフ化して画像として表示
- RP（ランクポイント）推移の可視化
- 直近の戦績差分を自動計算・表示
- 任意の日時を指定して戦績を比較（※実装予定）
- ユーザーごとの戦績履歴を JSON 形式で保存・管理

## ディレクトリ構成

```
APEX_Stats_Bot/
├── bot.py # Discord BOT のエントリーポイント
├── commands/
│ └── apex.py # スラッシュコマンド処理ロジック
├── data/
│ ├── dummy_data.py # ダミーデータ生成（テスト用）
│ └── storage.py # 履歴データの保存・取得機能
├── utils/
│ └── graph.py # グラフ描画（Kill/Match比・RP）
├── user_data/
│ └── ... # 各ユーザーの戦績履歴（JSON）
└── README.md # 本ドキュメント
```

## セットアップ・実行方法

### 1. このリポジトリをクローン

```bash
git clone https://github.com/your-username/apex-stats-discord-bot.git
cd apex-stats-discord-bot
```
### 2. 仮想環境を作成(任意)

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows
```

### 3. パッケージインストール
```bash
pip install -r requirements.txt
```

### 4. 仮想環境を設定
.envファイルに以下を記載
```
DISCORD_BOT_TOKEN=あなたのDiscordトークン
TRN_API_KEY=（任意。APIを使う場合のみ）
```

### 5. Botを起動
```bash
python bot.py
```

## TRN APIについて
本BOTは、[tracker.gg（TRN）](https://tracker.gg/developers)が提供するAPIを使ってAPEX Legendsの戦績を取得します。
TRN APIの利用にはアカウント登録とキー発行が必要です。

## 動作確認済環境
- Python 3.10+
- py-cord 2.x（discord.ext.commands / discord.commands）
- matplotlib

## 使い方

Discord上で `/apex` コマンドを使うと、Apex Legends のプレイヤーデータが表示されます。  
初回は基本ステータス（キル数、K/M、ランクなど）を取得し、以降は履歴と比較した「差分」もプライベートで通知されます。

### コマンド一覧

| コマンド | 引数 | 説明 |
|----------|------|------|
| `/apex` | `platform`, `username` | 指定ユーザーの現在のステータスと直近の差分を表示 |
| `/compare_apex`（予定） | `platform`, `username`, `日付` | 指定した日付との戦績比較を表示（開発中） |

※ `platform` には `origin`, `psn`, `xbl` のいずれかを指定してください。

---

## 開発メモ・今後の実装予定

現在は機能を段階的に実装中です。以下は対応中／予定の機能です：

### 実装済み
- Discordスラッシュコマンド対応
- 戦績のローカル保存・差分比較
- K/M・RP推移のグラフ化（画像送信）

### 今後の予定
- 任意日付を指定した差分比較コマンド
- ユーザー単位での戦績一覧表示
- SQLite または MongoDB によるデータ永続化
- WebUIまたはBotメニューによるユーザー設定画面

---

## クレジット

このBOTは非公式であり、EA や Respawn、tracker.gg とは一切関係ありません。