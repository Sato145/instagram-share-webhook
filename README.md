# Social Media Share Webhook

iPhoneの共有ボタンから受け取ったSNS URLを処理し、テンプレート化されたX投稿リンクをPushoverに通知するシステム

## 🎯 対応プラットフォーム

- ✅ **Instagram** (投稿/リール/ストーリー)
- ✅ **TikTok** (動画)
- 🔜 YouTube (予定)

## ✨ 機能

- ✅ iPhoneの共有ボタンからSNS URLを受信
- ✅ プラットフォーム自動検出（Instagram/TikTok）
- ✅ 投稿情報を自動取得（ユーザー名、本文、投稿タイプ）
- ✅ テンプレートに基づいたX投稿文を自動生成
- ✅ X投稿用のIntent URLを生成
- ✅ Pushoverに通知（X投稿リンク付き）
- ✅ Render無料サーバーで24時間稼働

## 🏗 システム構成

```
iPhone（Instagram/TikTok共有）
  ↓ ショートカットアプリ
  ↓ POST https://your-app.onrender.com/webhook
Renderサーバー（Python Flask）
  ↓ プラットフォーム検出
  ↓ 投稿情報取得
  ↓ テンプレート整形
  ↓ X投稿リンク生成
Pushover通知（X投稿リンク付き）
  ↓ タップ
Xアプリで投稿
```

## 📋 必要なもの

1. **Pushoverアカウント**
   - App Token
   - User Key

2. **Renderアカウント**（無料）
   - https://render.com

3. **iPhone**
   - ショートカットアプリ

## 🚀 セットアップ手順

### 1. Renderにデプロイ

#### 方法A: GitHubリポジトリから（推奨）

1. このプロジェクトをGitHubにプッシュ

2. Renderダッシュボードにアクセス
   - https://dashboard.render.com

3. 「New +」→「Web Service」をクリック

4. GitHubリポジトリを接続

5. 設定:
   - **Name**: `instagram-share-webhook`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: `Free`

6. 「Create Web Service」をクリック

#### 方法B: 手動デプロイ

1. Renderダッシュボードで「New +」→「Web Service」

2. 「Public Git repository」を選択

3. このリポジトリのURLを入力

4. 上記と同じ設定を入力

### 2. 環境変数を設定

Renderダッシュボードで:

1. 作成したサービスを選択

2. 「Environment」タブをクリック

3. 環境変数を追加:
   ```
   PUSHOVER_TOKEN = あなたのPushover App Token
   PUSHOVER_USER = あなたのPushover User Key
   ```

4. 「Save Changes」をクリック

### 3. デプロイ完了を確認

1. デプロイが完了するまで待つ（3-5分）

2. サービスURLを確認:
   ```
   https://your-app-name.onrender.com
   ```

3. ブラウザでアクセスして動作確認:
   ```json
   {
     "status": "ok",
     "service": "Instagram Share Webhook",
     "version": "1.0.0"
   }
   ```

### 4. iPhoneショートカットを設定

詳細は `SHORTCUT_SETUP.md` を参照

簡易手順:

1. ショートカットアプリを開く

2. 「+」→ 新規ショートカット作成

3. 「共有シートに表示」をON

4. 受け取る項目: `URL`

5. アクション追加:
   - 「辞書」を追加
     - キー: `url`
     - 値: `ショートカット入力`
   
   - 「URLの内容を取得」を追加
     - URL: `https://your-app-name.onrender.com/webhook`
     - メソッド: `POST`
     - 本文: `JSON`
     - 辞書を選択

6. ショートカット名: `Instagram共有`

7. 完了

## 📱 使い方

1. Instagramアプリで投稿を開く

2. 共有ボタン（紙飛行機アイコン）をタップ

3. 「Instagram共有」ショートカットを選択

4. 数秒後、Pushover通知が届く

5. 通知をタップ → Xアプリが開く

6. 投稿文を確認して投稿

## 🎨 テンプレートカスタマイズ

`app.py` の `create_tweet_text()` 関数を編集:

```python
def create_tweet_text(info):
    # 投稿タイプに応じた絵文字
    emoji = '🎬' if info['is_reel'] else '📷'
    
    # カスタムテンプレート
    tweet_text = f"{emoji} {info['username']}さんの{info['type']}\n\n{description}\n\n{info['url']}\n\n#Instagram"
    
    return tweet_text
```

変更後、Renderで自動再デプロイされます。

## 🔧 トラブルシューティング

### Pushover通知が届かない

- 環境変数が正しく設定されているか確認
- Pushover App TokenとUser Keyを再確認

### Instagram情報が取得できない

- 非公開アカウントの投稿は取得できません
- Instagramの仕様変更により取得できない場合があります

### Renderサービスがスリープする

- 無料プランは15分間アクセスがないとスリープします
- 初回アクセス時に10-30秒かかる場合があります
- 有料プラン（$7/月）でスリープを無効化できます

### ショートカットが動作しない

- URLが正しいか確認
- Renderサービスが起動しているか確認
- ショートカットのログを確認

## 📊 API仕様

### POST /webhook

Instagram URLを受け取って処理

**リクエスト:**
```json
{
  "url": "https://www.instagram.com/p/xxxxx/"
}
```

**レスポンス:**
```json
{
  "status": "success",
  "instagram_info": {
    "url": "https://www.instagram.com/p/xxxxx/",
    "username": "example_user",
    "type": "投稿"
  },
  "tweet_text": "📷 example_userさんの投稿\n\n...",
  "twitter_url": "https://twitter.com/intent/tweet?text=...",
  "notification_sent": true,
  "timestamp": "2026-02-21T12:00:00"
}
```

### GET /

ヘルスチェック

### GET /health

ヘルスチェック

## 🔒 セキュリティ

- 環境変数でPushover認証情報を管理
- HTTPS通信
- リクエスト検証

## 📝 ライセンス

MIT License

## 🙏 謝辞

- Flask
- Pushover
- Render
- BeautifulSoup4

---

作成日: 2026年2月21日
