# クイックスタートガイド

## 🚀 5分で始める

### 必要なもの

- ✅ Pushoverアカウント（App Token、User Key）
- ✅ GitHubアカウント
- ✅ Renderアカウント（無料）
- ✅ iPhone

### ステップ1: Pushover設定（1分）

1. https://pushover.net にアクセス

2. ログイン

3. 「Create an Application/API Token」をクリック

4. 以下をメモ:
   - **App Token**: `axxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - **User Key**: `uxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### ステップ2: GitHubにプッシュ（2分）

```bash
# プロジェクトディレクトリに移動
cd instagram-share-webhook

# Gitリポジトリを初期化
git init
git add .
git commit -m "Initial commit"

# GitHubにプッシュ
git remote add origin https://github.com/YOUR_USERNAME/instagram-share-webhook.git
git branch -M main
git push -u origin main
```

### ステップ3: Renderにデプロイ（2分）

1. https://dashboard.render.com にアクセス

2. 「New +」→「Web Service」

3. GitHubリポジトリを接続

4. 設定:
   - **Name**: `instagram-share-webhook`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: `Free`

5. 環境変数を追加:
   - `PUSHOVER_TOKEN`: あなたのApp Token
   - `PUSHOVER_USER`: あなたのUser Key

6. 「Create Web Service」をクリック

7. デプロイ完了を待つ（3-5分）

8. サービスURLをメモ:
   ```
   https://your-app-name.onrender.com
   ```

### ステップ4: iPhoneショートカット設定（3分）

1. ショートカットアプリを開く

2. 「+」→ 新規ショートカット

3. 右上「⋯」→「共有シートに表示」ON

4. 「共有シートのタイプ」→「URL」を選択

5. アクション追加:

   **辞書**:
   - キー: `url`
   - 値: `ショートカット入力`

   **URLの内容を取得**:
   - URL: `https://your-app-name.onrender.com/webhook`
   - メソッド: `POST`
   - 本文: `JSON`
   - 辞書を選択

6. ショートカット名: `Instagram共有`

7. 完了

### ステップ5: テスト（1分）

1. Instagramアプリを開く

2. 任意の投稿を開く

3. 共有ボタン（紙飛行機）をタップ

4. 「Instagram共有」を選択

5. Pushover通知が届く（10-30秒）

6. 通知をタップ → Xアプリが開く

7. 投稿文を確認して投稿

## ✅ 完了！

これで、iPhoneからInstagram投稿を簡単にXに共有できます。

## 📚 詳細ドキュメント

- [README.md](README.md) - 完全なドキュメント
- [RENDER_DEPLOY.md](RENDER_DEPLOY.md) - Renderデプロイ詳細
- [SHORTCUT_SETUP.md](SHORTCUT_SETUP.md) - ショートカット設定詳細

## 🔧 トラブルシューティング

### Pushover通知が届かない

→ Render環境変数を確認

### ショートカットが動作しない

→ URLが正しいか確認（末尾に `/webhook`）

### 初回が遅い

→ Renderの無料プランはスリープします（10-30秒で起動）

---

作成日: 2026年2月21日
