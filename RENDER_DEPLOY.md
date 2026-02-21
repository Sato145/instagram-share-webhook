# Renderデプロイガイド

## 🎯 概要

このガイドでは、Instagram Share WebhookをRenderの無料プランにデプロイする手順を説明します。

## 📋 前提条件

- GitHubアカウント
- Renderアカウント（無料）
- Pushover App TokenとUser Key

## 🚀 デプロイ手順

### ステップ1: GitHubリポジトリを作成

#### 1-1. GitHubで新規リポジトリ作成

1. https://github.com にアクセス

2. 右上の「+」→「New repository」をクリック

3. リポジトリ設定:
   - **Repository name**: `instagram-share-webhook`
   - **Description**: `Instagram共有からX投稿を支援するWebhook`
   - **Public** または **Private**（どちらでもOK）
   - **Initialize this repository with**: チェックなし

4. 「Create repository」をクリック

#### 1-2. ローカルからプッシュ

```bash
# プロジェクトディレクトリに移動
cd instagram-share-webhook

# Gitリポジトリを初期化
git init

# ファイルを追加
git add .

# コミット
git commit -m "Initial commit: Instagram Share Webhook"

# リモートリポジトリを追加
git remote add origin https://github.com/YOUR_USERNAME/instagram-share-webhook.git

# プッシュ
git branch -M main
git push -u origin main
```

### ステップ2: Renderアカウント作成

1. https://render.com にアクセス

2. 「Get Started」をクリック

3. GitHubアカウントで登録（推奨）
   - 「Sign up with GitHub」をクリック
   - GitHubの認証を許可

4. メールアドレスを確認

### ステップ3: Renderに新規サービスを作成

#### 3-1. ダッシュボードにアクセス

1. https://dashboard.render.com にアクセス

2. 「New +」ボタンをクリック

3. 「Web Service」を選択

#### 3-2. GitHubリポジトリを接続

1. 「Connect a repository」セクションで:
   - GitHubアカウントを接続（初回のみ）
   - リポジトリ一覧から `instagram-share-webhook` を選択
   - 「Connect」をクリック

2. リポジトリが見つからない場合:
   - 「Configure account」をクリック
   - Renderにリポジトリへのアクセス権を付与

#### 3-3. サービス設定

以下の設定を入力:

| 項目 | 値 |
|------|-----|
| **Name** | `instagram-share-webhook` |
| **Region** | `Singapore (Southeast Asia)` または `Oregon (US West)` |
| **Branch** | `main` |
| **Root Directory** | （空白） |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Plan** | `Free` |

#### 3-4. 環境変数を設定

「Environment Variables」セクションで:

1. 「Add Environment Variable」をクリック

2. 変数1:
   - **Key**: `PUSHOVER_TOKEN`
   - **Value**: あなたのPushover App Token

3. 「Add Environment Variable」をクリック

4. 変数2:
   - **Key**: `PUSHOVER_USER`
   - **Value**: あなたのPushover User Key

#### 3-5. デプロイ開始

1. 「Create Web Service」をクリック

2. デプロイが開始されます（3-5分かかります）

3. ログを確認:
   ```
   ==> Building...
   ==> Installing dependencies...
   ==> Starting server...
   ==> Your service is live 🎉
   ```

### ステップ4: デプロイ確認

#### 4-1. サービスURLを確認

デプロイ完了後、以下のようなURLが発行されます:

```
https://instagram-share-webhook-xxxx.onrender.com
```

#### 4-2. 動作確認

1. ブラウザでサービスURLにアクセス

2. 以下のようなJSONが表示されればOK:
   ```json
   {
     "status": "ok",
     "service": "Instagram Share Webhook",
     "version": "1.0.0",
     "endpoints": {
       "webhook": "/webhook (POST)",
       "health": "/ (GET)"
     }
   }
   ```

#### 4-3. Webhook エンドポイントをテスト

curlコマンドでテスト:

```bash
curl -X POST https://your-app-name.onrender.com/webhook \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.instagram.com/p/C3xXxXxXxXx/"}'
```

成功すると:
```json
{
  "status": "success",
  "instagram_info": {
    "url": "https://www.instagram.com/p/C3xXxXxXxXx/",
    "username": "example_user",
    "type": "投稿"
  },
  "tweet_text": "📷 example_userさんの投稿...",
  "twitter_url": "https://twitter.com/intent/tweet?text=...",
  "notification_sent": true,
  "timestamp": "2026-02-21T12:00:00"
}
```

Pushover通知も届くはずです。

## 🔧 Renderダッシュボードの使い方

### ログを確認

1. サービスを選択

2. 「Logs」タブをクリック

3. リアルタイムログが表示されます

### 環境変数を変更

1. サービスを選択

2. 「Environment」タブをクリック

3. 変数を編集

4. 「Save Changes」をクリック

5. サービスが自動的に再起動されます

### 手動で再デプロイ

1. サービスを選択

2. 右上の「Manual Deploy」→「Deploy latest commit」をクリック

### サービスを削除

1. サービスを選択

2. 「Settings」タブをクリック

3. 下部の「Delete Web Service」をクリック

## 📊 Render無料プランの制限

### 制限事項

- **スリープ**: 15分間アクセスがないとスリープ
- **起動時間**: スリープから起動に10-30秒かかる
- **月間稼働時間**: 750時間/月（約31日）
- **帯域幅**: 100GB/月
- **ビルド時間**: 500分/月

### 制限の影響

- 初回アクセス時に遅延が発生する可能性
- 頻繁に使用する場合は問題なし
- 月間750時間を超える場合は有料プラン検討

### 有料プランへのアップグレード

スリープを無効化したい場合:

1. サービスを選択

2. 「Settings」タブをクリック

3. 「Plan」セクションで「Starter」を選択（$7/月）

4. 「Update Plan」をクリック

## 🔄 自動デプロイ設定

Renderは自動的にGitHubと連携しています:

1. GitHubにプッシュ
   ```bash
   git add .
   git commit -m "Update template"
   git push
   ```

2. Renderが自動的に検知

3. 自動的に再デプロイ

4. 数分後に変更が反映

## 🔒 セキュリティ設定

### 環境変数の管理

- 環境変数はGitにコミットしない
- Renderダッシュボードでのみ設定
- `.gitignore` に `.env` を追加済み

### HTTPS通信

- Renderは自動的にHTTPSを提供
- 証明書の更新も自動

### アクセス制限（オプション）

特定のIPからのみアクセスを許可したい場合:

`app.py` に以下を追加:

```python
ALLOWED_IPS = ['xxx.xxx.xxx.xxx']

@app.before_request
def limit_remote_addr():
    if request.remote_addr not in ALLOWED_IPS:
        abort(403)
```

## 🐛 トラブルシューティング

### デプロイが失敗する

**原因**: `requirements.txt` の依存関係エラー

**解決方法**:
1. ローカルで動作確認
   ```bash
   pip install -r requirements.txt
   python app.py
   ```
2. エラーを修正
3. GitHubにプッシュ

### サービスが起動しない

**原因**: `gunicorn` の設定エラー

**解決方法**:
1. Renderログを確認
2. `Start Command` が `gunicorn app:app` になっているか確認
3. `requirements.txt` に `gunicorn` が含まれているか確認

### 環境変数が反映されない

**原因**: サービスが再起動されていない

**解決方法**:
1. 環境変数を変更後、「Save Changes」をクリック
2. サービスが自動的に再起動されるまで待つ
3. 手動で再デプロイも可能

### Pushover通知が届かない

**原因**: 環境変数が間違っている

**解決方法**:
1. Renderダッシュボードで環境変数を確認
2. Pushover App TokenとUser Keyを再確認
3. Pushoverダッシュボードで通知履歴を確認

## 📈 モニタリング

### Renderダッシュボード

- **Metrics**: CPU、メモリ、リクエスト数
- **Logs**: リアルタイムログ
- **Events**: デプロイ履歴

### 外部モニタリング（オプション）

UptimeRobotなどで定期的にヘルスチェック:

```
https://your-app-name.onrender.com/health
```

5分ごとにアクセスすることで、スリープを防ぐことも可能。

## 🔗 参考リンク

- [Render公式ドキュメント](https://render.com/docs)
- [Render無料プラン詳細](https://render.com/docs/free)
- [Python on Render](https://render.com/docs/deploy-flask)
- [環境変数の管理](https://render.com/docs/environment-variables)

---

最終更新: 2026年2月21日
