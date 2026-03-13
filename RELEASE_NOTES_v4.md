# バージョン4.0.0 リリースノート

## 🎉 メジャーアップデート

主要SNSプラットフォームに対応し、合計7つのプラットフォームをサポートするようになりました！

## 🆕 新規対応プラットフォーム

### 1. X (Twitter)
- ポストの共有に対応
- 対応URL:
  - `https://twitter.com/username/status/xxxxx`
  - `https://x.com/username/status/xxxxx`
- 絵文字: 🐦

### 2. Threads
- スレッドの共有に対応
- 対応URL:
  - `https://www.threads.net/@username/post/xxxxx`
- 絵文字: 🧵

### 3. Facebook
- 投稿の共有に対応
- 対応URL:
  - `https://www.facebook.com/username/posts/xxxxx`
  - `https://www.facebook.com/username/videos/xxxxx`
- 絵文字: 👍

### 4. LinkedIn
- 投稿の共有に対応
- 対応URL:
  - `https://www.linkedin.com/posts/username_xxxxx`
  - `https://www.linkedin.com/feed/update/urn:li:activity:xxxxx`
- 絵文字: 💼

## 📊 対応プラットフォーム一覧

| プラットフォーム | 絵文字 | 投稿タイプ |
|----------------|--------|-----------|
| Instagram | 📷/🎬 | 投稿/リール/ストーリー |
| TikTok | 🎵 | 動画 |
| YouTube | 🎥 | 動画/Shorts |
| X (Twitter) | 🐦 | ポスト |
| Threads | 🧵 | スレッド |
| Facebook | 👍 | 投稿 |
| LinkedIn | 💼 | 投稿 |

## ✨ 機能

すべてのプラットフォームで以下の機能が利用可能：

- ✅ URL自動検出
- ✅ ユーザー名自動抽出
- ✅ ユーザー名ベースのハッシュタグ
- ✅ 追加カスタムハッシュタグ
- ✅ 投稿本文の自動取得（可能な場合）
- ✅ X投稿用Intent URL生成
- ✅ Pushover通知

## 🎯 使い方

### 基本的な使い方

1. 各SNSアプリで投稿を開く
2. 共有ボタンをタップ
3. 「SNS共有」ショートカットを選択
4. Pushover通知が届く
5. 通知をタップしてXに投稿

### ハッシュタグの構成

```
#ユーザー名 #追加タグ1 #追加タグ2 ...
```

- ユーザー名が自動的にベースハッシュタグになります
- `hashtags`パラメータで追加のハッシュタグを指定できます

### 例

#### X (Twitter) ポストを共有

**入力:**
```
URL: https://twitter.com/username/status/1234567890
hashtags: 話題 トレンド
```

**生成される投稿文:**
```
🐦 usernameのポスト

興味深い内容！

https://twitter.com/username/status/1234567890

#username #話題 #トレンド
```

#### Threads スレッドを共有

**入力:**
```
URL: https://www.threads.net/@username/post/xxxxx
hashtags: Threads Meta
```

**生成される投稿文:**
```
🧵 usernameのスレッド

面白いスレッド！

https://www.threads.net/@username/post/xxxxx

#username #Threads #Meta
```

#### Facebook 投稿を共有

**入力:**
```
URL: https://www.facebook.com/username/posts/1234567890
hashtags: Facebook SNS
```

**生成される投稿文:**
```
👍 usernameの投稿

チェックしてみて！

https://www.facebook.com/username/posts/1234567890

#username #Facebook #SNS
```

#### LinkedIn 投稿を共有

**入力:**
```
URL: https://www.linkedin.com/posts/username_xxxxx
hashtags: ビジネス キャリア
```

**生成される投稿文:**
```
💼 usernameの投稿

参考になる投稿！

https://www.linkedin.com/posts/username_xxxxx

#username #ビジネス #キャリア
```

## 🔧 技術的な変更

### 新規ファイル

- `services/x_service.py` - X情報取得サービス
- `services/threads_service.py` - Threads情報取得サービス
- `services/facebook_service.py` - Facebook情報取得サービス
- `services/linkedin_service.py` - LinkedIn情報取得サービス
- `test_all_platforms.py` - 全プラットフォームテスト

### 更新ファイル

- `app.py` - 新プラットフォーム対応
- `services/common.py` - プラットフォーム検出を拡張
- `README.md` - 対応プラットフォームを更新
- `CHANGELOG.md` - v4.0.0の変更内容を追加
- `PROJECT_SUMMARY.md` - 最新情報に更新
- `USAGE_GUIDE.md` - 全プラットフォームの使い方を追加

## 📈 パフォーマンス

- 処理時間: 各プラットフォーム2-5秒
- メモリ使用量: 約50-100MB（変更なし）

## 🔄 移行ガイド

### 既存ユーザー向け

#### ステップ1: コードを更新

```bash
cd instagram-share-webhook
git pull origin main
```

#### ステップ2: Renderで再デプロイ

1. Renderダッシュボードを開く
2. サービスを選択
3. 「Manual Deploy」→「Deploy latest commit」

#### ステップ3: 動作確認

新しいプラットフォームで動作確認：

```bash
# ローカルでテスト
python3 app.py

# 別のターミナルで
python3 test_all_platforms.py
```

既存のショートカットはそのまま動作します。

## 🐛 既知の問題

1. **非公開アカウント**
   - 非公開アカウントの投稿は情報取得できません
   - 公開アカウントのみ対象

2. **プラットフォームの仕様変更**
   - 各プラットフォームの仕様変更により、情報取得できない場合があります
   - その場合は、`username`と`caption`パラメータで手動指定可能

## 💡 ヒント

- すべてのプラットフォームで同じショートカットが使えます
- プラットフォームは自動検出されます
- ユーザー名が取得できない場合は、`username`パラメータで指定可能
- 追加のハッシュタグは`hashtags`パラメータで指定

## 🙏 フィードバック

問題や改善案があれば、GitHubのIssueで報告してください。

## 📚 関連ドキュメント

- [README.md](README.md) - プロジェクト概要
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - 詳細な使い方ガイド
- [HASHTAG_FEATURE.md](HASHTAG_FEATURE.md) - ハッシュタグ機能ガイド
- [SHORTCUT_SETUP.md](SHORTCUT_SETUP.md) - ショートカット設定ガイド
- [CHANGELOG.md](CHANGELOG.md) - 変更履歴

---

バージョン4.0.0へのアップデート、お疲れ様でした！
7つのSNSプラットフォームをお楽しみください！
