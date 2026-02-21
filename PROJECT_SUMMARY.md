# Instagram Share Webhook - プロジェクトサマリー

## 📋 プロジェクト概要

iPhoneの共有ボタンから受け取ったInstagram URLを処理し、テンプレート化されたX投稿リンクをPushoverに通知するシステム

## 🎯 目的

Instagram投稿を見つけたら、ワンタップでX投稿文を生成し、簡単にXに共有できるようにする

## 🏗 システム構成

```
iPhone（Instagram共有）
  ↓ ショートカットアプリ
  ↓ POST https://your-app.onrender.com/webhook
Renderサーバー（Python Flask）
  ↓ Instagram投稿情報取得
  ↓ テンプレート整形
  ↓ X投稿リンク生成
Pushover通知（X投稿リンク付き）
  ↓ タップ
Xアプリで投稿
```

## ✨ 主な機能

1. **Instagram情報自動取得**
   - ユーザー名
   - 投稿本文
   - 投稿タイプ（投稿/リール/ストーリー）
   - 画像URL

2. **テンプレート整形**
   - 投稿タイプに応じた絵文字
   - 本文の自動短縮（100文字）
   - ハッシュタグ自動付与

3. **X投稿リンク生成**
   - Twitter Intent URL
   - URLエンコード処理

4. **Pushover通知**
   - リンク付き通知
   - タップでXアプリが開く

## 📁 ファイル構成

```
instagram-share-webhook/
├── app.py                    # メインアプリケーション
├── requirements.txt          # 本番環境用パッケージ
├── requirements-dev.txt      # 開発環境用パッケージ
├── render.yaml              # Render設定ファイル
├── .gitignore               # Git除外設定
├── .env.example             # 環境変数テンプレート
├── test_local.py            # ローカルテストスクリプト
├── README.md                # 完全なドキュメント
├── QUICKSTART.md            # クイックスタートガイド
├── RENDER_DEPLOY.md         # Renderデプロイガイド
├── SHORTCUT_SETUP.md        # iPhoneショートカット設定ガイド
└── PROJECT_SUMMARY.md       # このファイル
```

## 🔧 技術スタック

### バックエンド
- **Python 3.9+**
- **Flask 3.0.0** - Webフレームワーク
- **Gunicorn 21.2.0** - WSGIサーバー
- **Requests 2.31.0** - HTTP通信
- **BeautifulSoup4 4.12.2** - HTMLパース

### インフラ
- **Render** - ホスティング（無料プラン）
- **GitHub** - ソースコード管理

### 通知
- **Pushover API** - プッシュ通知

### クライアント
- **iPhoneショートカット** - 共有機能

## 🚀 デプロイ方法

### 1. ローカルテスト

```bash
# 依存関係インストール
pip install -r requirements-dev.txt

# 環境変数設定
cp .env.example .env
# .env を編集

# サーバー起動
python app.py

# テスト実行
python test_local.py
```

### 2. Renderにデプロイ

```bash
# GitHubにプッシュ
git init
git add .
git commit -m "Initial commit"
git push -u origin main

# Renderダッシュボードで:
# 1. New Web Service
# 2. GitHubリポジトリを接続
# 3. 環境変数を設定
# 4. デプロイ
```

### 3. iPhoneショートカット設定

詳細は `SHORTCUT_SETUP.md` を参照

## 📊 API仕様

### POST /webhook

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

## 🎨 カスタマイズポイント

### 1. テンプレート変更

`app.py` の `create_tweet_text()` 関数:

```python
def create_tweet_text(info):
    # カスタムテンプレート
    tweet_text = f"あなたのテンプレート"
    return tweet_text
```

### 2. ハッシュタグ変更

```python
tweet_text = f"...\n\n#YourHashtag"
```

### 3. 絵文字変更

```python
emoji = '🎬' if info['is_reel'] else '📷'
```

### 4. 本文短縮文字数変更

```python
if len(description) > 100:  # ← この数字を変更
    description = description[:100] + '...'
```

## 💰 コスト

### 無料で運用可能

- **Render**: 無料プラン（750時間/月）
- **Pushover**: 無料（iOS/Android $5買い切り）
- **GitHub**: 無料
- **iPhoneショートカット**: 無料

### 有料オプション

- **Render Starter**: $7/月（スリープなし）
- **Render Pro**: $25/月（より高性能）

## 📈 制限事項

### Render無料プラン

- 15分間アクセスがないとスリープ
- 起動に10-30秒かかる
- 月間750時間（約31日）
- 帯域幅100GB/月

### Instagram情報取得

- 非公開アカウントは取得不可
- Instagramの仕様変更により取得できない場合あり
- レート制限あり

## 🔒 セキュリティ

- HTTPS通信
- 環境変数で認証情報管理
- Gitに認証情報をコミットしない
- Renderの自動SSL証明書

## 🐛 既知の問題

1. **初回アクセスが遅い**
   - Renderの無料プランはスリープする
   - 解決策: 有料プランにアップグレード

2. **Instagram情報が取得できない**
   - 非公開アカウントまたは仕様変更
   - 解決策: 公開アカウントのみ対象

3. **Pushover通知が届かない**
   - 環境変数が間違っている
   - 解決策: Render環境変数を確認

## 🔮 今後の拡張案

### 短期

- [ ] 複数のテンプレート選択機能
- [ ] 画像URLの取得と添付
- [ ] ユーザー別のカスタムテンプレート

### 中期

- [ ] X自動投稿機能（X API連携）
- [ ] 投稿履歴の保存
- [ ] 統計情報の表示

### 長期

- [ ] 複数SNS対応（TikTok、YouTube等）
- [ ] AI要約機能（OpenAI連携）
- [ ] Webダッシュボード

## 📚 参考資料

- [Flask公式ドキュメント](https://flask.palletsprojects.com/)
- [Render公式ドキュメント](https://render.com/docs)
- [Pushover API](https://pushover.net/api)
- [Twitter Intent URL](https://developer.twitter.com/en/docs/twitter-for-websites/tweet-button/guides/web-intent)
- [iPhoneショートカット](https://support.apple.com/ja-jp/guide/shortcuts/welcome/ios)

## 🙏 謝辞

- Flask開発チーム
- Render
- Pushover
- BeautifulSoup4開発チーム

## 📝 ライセンス

MIT License

## 👤 作成者

作成日: 2026年2月21日
作成者: Kiro AI Assistant

## 📞 サポート

問題が発生した場合:

1. `README.md` を確認
2. `RENDER_DEPLOY.md` でデプロイ手順を確認
3. `SHORTCUT_SETUP.md` でショートカット設定を確認
4. Renderログを確認
5. ローカルでテスト実行

---

このプロジェクトは、Instagram投稿をXに簡単に共有するための個人利用ツールです。
