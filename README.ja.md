# NovelGame

> **ストーリー設定を二度と説明し直さなくていい。** AI エージェント向けの自己完結型インタラクティブ・フィクション・エンジン——世界観・キャラクター・ルールを一度パッケージ化すれば、AI が毎セッション自動で読み込み、進行状況はコンテキスト消失後も失われません。

**この README の言語:** [English](README.md) · [中文](README.zh-CN.md) · [日本語](README.ja.md)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Agent Plugins](https://img.shields.io/badge/Agent%20Plugins-1.0.0-blue.svg)](https://agent-plugins.org)
[![Output Languages](https://img.shields.io/badge/Output-EN%20%7C%20%E4%B8%AD%E6%96%87%20%7C%20%E6%97%A5%E6%9C%AC%E8%AA%9E-blue.svg)](README.md)
[![Zero Dependencies](https://img.shields.io/badge/Zero%20Dependencies-Yes-brightgreen.svg)](skills/novel-game/scripts/state.py)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)](CONTRIBUTING.md)

[Agent Plugins](https://agent-plugins.org) 1.0.0 仕様に基づいて構築（Working Draft）。

## なぜ NovelGame なのか？

| 痛点 | 通常の AI チャット | NovelGame の場合 |
|------|--------------------|------------------|
| **設定の再説明** | 毎セッション、世界観・キャラ・ルールを口頭で再説明（「毎回設定に半日かかる」） | 設定はファイル——一度書けば、毎回自動ロード |
| **進行状況の消失** | コンテキスト圧縮や新規チャットでストーリー状態が消える | 状態はディスク上の JSON セーブに永続化。章スナップショット＋動的コンテキスト注入で復元——復元は再開であってリセットではない |
| **AI 臭い文章** | ありきたりでテンプレ的な文体 | アンチ・テンプレ・エンジン：定型句ブラックリスト、感覚優先の執筆ルール、非定型プロット集、ナラティブ品質の自己評価 |

## 機能

- **設定はファイル** — 世界観を一度書けば、毎セッション自動ロード。
- **状態はスクリプト** — 進行状況・好感度・インベントリ・フラグ・分岐履歴を `state.py` で JSON セーブに永続化。コンテキスト消失や新規セッションでも状態は生き残る。
- **階層型メモリ** — 短期（直近の出来事）・中期（章の要約）・長期（プレイヤー好みの振り返り）の 3 層で長編の整合性を維持。
- **章スナップショット＋動的コンテキスト注入** — コンテキスト圧縮や新規セッション後もシームレスに復元。復元は再開であってリセットではない。
- **ToT 分岐計画** — 内部で 3〜5 の展開を評価し、最強の 2〜4 択だけを残す。
- **ナラティブ品質スコアリング** — 各出力を OOC・設定整合性・一貫性・アンチ・テンプレ強度・選択肢品質で自己評価。
- **アンチ・テンプレ・エンジン** — 定型句ブラックリスト、感覚優先の執筆ルール、非定型プロット集で AI 臭い文章を回避。
- **英語優先・多言語出力** — エンジンのルールとコマンドは英語で正確に。物語本文は**英語・中国語・日本語**を切替可能。

## 言語サポート

| 言語 | コード | 物語出力 |
|------|--------|----------|
| 英語（デフォルト） | `en` | 対応 |
| 中国語 | `zh` | 対応 |
| 日本語 | `ja` | 対応 |

- エンジンのルール・コマンド・スクリプト出力は常に英語（指示の曖昧さを排除）。
- 設定ファイルでデフォルト言語を指定（`## Language: en|zh|ja`）、または会話中に "switch to Chinese"、"用中文"、"日本語に切り替えて" などで即時切替。
- 設定ファイルは英語・中国語・日本語のいずれでも記述可能。初期状態パーサーは 3 言語すべてを認識。

## クイックスタート

```bash
# 1. 設定テンプレートをコピーして記入
cp skills/novel-game/references/SETTINGS.md my_story.md

# 2. 設定からセーブを初期化
python3 skills/novel-game/scripts/new_story.py --settings my_story.md --title "My Story" --dir ./saves

# 3. プレイ開始——エンジンは毎ターン状態を読み込む
python3 skills/novel-game/scripts/state.py summary --dir ./saves
```

同梱のサンプルですぐ始める場合：

```bash
python3 skills/novel-game/scripts/new_story.py \
  --settings skills/novel-game/references/EXAMPLE.md \
  --title "The Fogbound Detective" --dir ./saves
```

## デモ

同梱サンプル『霧都の探偵』の 1 ターン（日本語出力）：

> **あなた**（法医学者の Erin に）：「埠頭の倉庫火災の事件ファイルを見せてほしい。」
>
> **NovelGame** — *Erin は目を細め、マニラフォルダーをテーブル越しに滑らせた。指先が端に留まる。「あの火事は事故じゃない。誰かがあの記録を消したがってる」*（好感度 +5）
>
> 1. 灰の中から何を見つけたのか尋ねる。
> 2. フォルダーを手に取り、何も言わずに立ち去る。
> 3. 彼女の判断を信じていると伝える——本気で。

エンジンは Erin への好感度を記録し、インベントリを更新し、イベントをログに残しました——すべて JSON セーブに永続化され、次回セッションでそのまま続きから遊べます。

## リポジトリ構成

```
novel-game/
├── LICENSE                     # Apache License 2.0
├── README.md                   # 英語 README
├── README.zh-CN.md             # 中国語 README
├── README.ja.md                # 日本語 README
├── CONTRIBUTING.md
├── CHANGELOG.md
├── .gitignore
├── plugin.json                 # Agent Plugins manifest
└── skills/
    └── novel-game/
        ├── SKILL.md            # エンジン指示（英語）
        ├── scripts/
        │   ├── state.py        # 状態管理 CLI（JSON セーブ）
        │   └── new_story.py    # 設定ファイルからセーブを初期化
        └── references/
            ├── SETTINGS.md     # ストーリー設定テンプレート
            ├── RULES.md        # エンジン必須ルール
            ├── ANTI_TROPE.md   # アンチ・テンプレ・チェックリスト＆プロット集
            └── EXAMPLE.md      # すぐ遊べるサンプルストーリー
```

## 状態コマンドリファレンス

```
python3 scripts/state.py init --title <title> [--settings <file>] [--dir <dir>]   # セーブ作成
python3 scripts/state.py get [--story <id>] [--dir <dir>]                        # 全状態を読む
python3 scripts/state.py summary [--story <id>] [--dir <dir>]                    # コンパクトな状態要約
python3 scripts/state.py set --key <flag> --value <value> [--dir <dir>]          # フラグ設定
python3 scripts/state.py add-stat --key <stat> --delta <delta> [--dir <dir>]     # 数値調整
python3 scripts/state.py add-item --item <item> [--dir <dir>]                    # インベントリ追加
python3 scripts/state.py remove-item --item <item> [--dir <dir>]                 # インベントリ削除
python3 scripts/state.py set-node --node <node> [--dir <dir>]                    # 現在ノード設定
python3 scripts/state.py log --event <event> [--dir <dir>]                       # イベント記録
python3 scripts/state.py remember --tier <short|mid|long> --content <content> [--dir <dir>]
python3 scripts/state.py recall --tier <short|mid|long> [--keyword <word>] [--limit N] [--dir <dir>]
python3 scripts/state.py reflect --content <reflection> [--dir <dir>]            # プレイヤー好みの振り返り
python3 scripts/state.py snapshot --scene <scene> --characters <chars> --goal <goal> --threads <threads> [--dir <dir>]
python3 scripts/state.py restore [--dir <dir>]                                    # 最新スナップショットから復元
python3 scripts/state.py context [--dir <dir>]                                    # 復元用の完全コンテキスト
python3 scripts/state.py list [--dir <dir>]                                      # セーブ一覧
```

セーブディレクトリ優先順位：`--dir` 引数 > `$NOVEL_DATA_DIR` > `./saves`。

## 要件

- Python 3.10+（標準ライブラリのみ、サードパーティ依存なし）

## プロジェクトを支援する

NovelGame が「設定の再説明」を一度でも減らしてくれたなら：

- **このリポジトリに Star を付ける** — 他の人に見つけてもらう最良の方法です。
- AI でインタラクティブ・フィクションを遊ぶ・書く友人に**シェア**する。
- Issues で**バグ報告**や**機能要望**を送る。
- **コントリビュート** — 始め方は [CONTRIBUTING.md](CONTRIBUTING.md) を参照。

## ライセンス

[Apache License 2.0](LICENSE)
