# ローカル開発ガイド

## 🛠 開発環境セットアップ

### 前提条件

- Python 3.9以上
- pip
- Git

### セットアップ手順

```bash
# プロジェクトディレクトリに移動
cd instagram-share-webhook

# 仮想環境作成（推奨）
python -m venv venv

# 仮想環境を有効化
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 依存関係インストール
pip install -r requirements-dev.txt

# 環境変数設定
cp .env.example .env
# .env を編集してPushover認証情報を入力
```

### .env ファイル設定

`.env` ファイルを編集:

```bash
# Pushover設定
PUSHOVER_TOKEN=あなたのPushover App Token
PUSHOVER_USER=あなたのPushover User Key

# サーバー設定
PORT=5000
FLASK_ENV=development
```

## 🚀 ローカルサーバー起動

### 方法1: Flaskの開発サーバー（推奨）

```bash
python app.py
```

サーバーが起動:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: off
```

### 方法2: Gunicorn（本番環境と同じ）

```bash
gunicorn app:app
```

## 🧪 テスト方法

### 自動テストスクリプト

```bash
python test_local.py
```

出力例:
```
============================================================
Instagram Share Webhook - ローカルテスト
============================================================

============================================================
ヘルスチェック
============================================================

ステータスコード: 200

レスポンス:
{
  "status": "healthy",
  "timestamp": "2026-02-21T12:00:00"
}

✅ サーバーは正常に動作しています

============================================================
テスト 1/2
============================================================

サーバーURL: http://localhost:5000
Instagram URL: https://www.instagram.com/p/C3xXxXxXxXx/

ステータスコード: 200

レスポンス:
{
  "status": "success",
  ...
}

✅ テスト成功！
Pushover通知を確認してください
```

### 手動テスト（curl）

#### ヘルスチェック

```bash
curl http://localhost:5000/health
```

#### Webhook テスト

```bash
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.instagram.com/p/C3xXxXxXxXx/"}'
```

#### リールのテスト

```bash
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.instagram.com/reel/C3xXxXxXxXx/"}'
```

### ブラウザでテスト

1. ブラウザで http://localhost:5000 を開く

2. 以下のようなJSONが表示されればOK:
   ```json
   {
     "status": "ok",
     "service": "Instagram Share Webhook",
     "version": "1.0.0"
   }
   ```

## 🔍 デバッグ

### ログ出力

`app.py` にログを追加:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 使用例
logger.debug(f"Instagram URL: {instagram_url}")
logger.info(f"Processing request")
logger.error(f"Error: {e}")
```

### Flaskデバッグモード

`app.py` の最後を変更:

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # debug=True
```

デバッグモードの機能:
- コード変更時に自動リロード
- 詳細なエラーメッセージ
- インタラクティブデバッガー

### Pythonデバッガー

ブレークポイントを設定:

```python
def webhook():
    data = request.get_json()
    
    import pdb; pdb.set_trace()  # ← ここで停止
    
    instagram_url = data.get('url', '')
```

## 📝 コード変更

### テンプレートを変更

`app.py` の `create_tweet_text()` 関数を編集:

```python
def create_tweet_text(info):
    # 投稿タイプに応じた絵文字
    emoji = '🎬' if info['is_reel'] else '📷'
    
    # カスタムテンプレート
    tweet_text = f"{emoji} {info['username']}さんの{info['type']}\n\n{info['description']}\n\n{info['url']}\n\n#Instagram"
    
    return tweet_text
```

変更後、サーバーを再起動（デバッグモードなら自動）。

### Instagram情報取得を改善

`app.py` の `extract_instagram_info()` 関数を編集:

```python
def extract_instagram_info(url):
    # カスタム処理を追加
    # ...
    return info
```

## 🧹 コード品質

### フォーマット（Black）

```bash
pip install black
black app.py
```

### リント（Flake8）

```bash
pip install flake8
flake8 app.py
```

### 型チェック（mypy）

```bash
pip install mypy
mypy app.py
```

## 📦 依存関係管理

### 新しいパッケージを追加

```bash
# インストール
pip install package-name

# requirements.txt に追加
pip freeze > requirements.txt
```

### 依存関係を更新

```bash
pip install --upgrade -r requirements.txt
```

## 🔄 Git ワークフロー

### 変更をコミット

```bash
git add .
git commit -m "Update template"
git push
```

### ブランチを作成

```bash
git checkout -b feature/new-template
# 変更を加える
git add .
git commit -m "Add new template"
git push -u origin feature/new-template
```

## 🚢 デプロイ前チェックリスト

- [ ] ローカルテストが成功
- [ ] `.env` ファイルがGitにコミットされていない
- [ ] `requirements.txt` が最新
- [ ] `README.md` が更新されている
- [ ] コードがフォーマットされている
- [ ] エラーハンドリングが適切

## 🐛 よくある問題

### ModuleNotFoundError

**原因**: 依存関係がインストールされていない

**解決方法**:
```bash
pip install -r requirements-dev.txt
```

### Port already in use

**原因**: ポート5000が既に使用されている

**解決方法**:
```bash
# 別のポートを使用
PORT=5001 python app.py

# または、使用中のプロセスを終了
lsof -ti:5000 | xargs kill -9
```

### Pushover通知が届かない

**原因**: 環境変数が設定されていない

**解決方法**:
```bash
# .env ファイルを確認
cat .env

# 環境変数を確認
echo $PUSHOVER_TOKEN
echo $PUSHOVER_USER
```

### Instagram情報が取得できない

**原因**: 非公開アカウントまたはネットワークエラー

**解決方法**:
- 公開アカウントの投稿でテスト
- ネットワーク接続を確認
- User-Agentを変更

## 📚 参考資料

- [Flask公式ドキュメント](https://flask.palletsprojects.com/)
- [Python公式ドキュメント](https://docs.python.org/3/)
- [Requests公式ドキュメント](https://requests.readthedocs.io/)
- [BeautifulSoup4公式ドキュメント](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

---

最終更新: 2026年2月21日
