# 変更履歴

## [4.0.0] - 2026-03-12

### 追加
- ✅ X (Twitter) のシェアに対応
  - ポストURL (`twitter.com/username/status/xxxxx`)
  - 新ドメイン (`x.com/username/status/xxxxx`)
- ✅ Threads のシェアに対応
  - スレッドURL (`threads.net/@username/post/xxxxx`)
- ✅ Facebook のシェアに対応
  - 投稿URL (`facebook.com/username/posts/xxxxx`)
  - 動画URL (`facebook.com/username/videos/xxxxx`)
- ✅ LinkedIn のシェアに対応
  - 投稿URL (`linkedin.com/posts/username_xxxxx`)

### 変更
- 📝 対応プラットフォームが7つに拡大
- 📝 READMEを更新

### 技術的な変更
- 新規ファイル: `services/x_service.py`
- 新規ファイル: `services/threads_service.py`
- 新規ファイル: `services/facebook_service.py`
- 新規ファイル: `services/linkedin_service.py`
- 更新: `services/common.py` - プラットフォーム検出を拡張
- 更新: `app.py` - 新プラットフォーム対応

## [3.0.0] - 2026-03-12

### 追加
- ✅ YouTube動画のシェアに対応
  - 通常の動画URL (`youtube.com/watch?v=`)
  - 短縮URL (`youtu.be/`)
  - Shorts (`youtube.com/shorts/`)
- ✅ カスタムハッシュタグ機能
  - ショートカットから `hashtags` パラメータで指定可能
  - `#`記号なしで入力（自動的に付与）
  - 複数のハッシュタグをスペース区切りで指定可能
  - 例: `STU48 アイドル 瀬戸内` → `#STU48 #アイドル #瀬戸内`

### 変更
- 📝 ショートカット設定ガイドを更新
  - カスタムハッシュタグの使い方を追加
  - YouTube対応の説明を追加
  - プラットフォーム別のテスト方法を追加
- 📝 READMEを更新
  - 対応プラットフォームにYouTubeを追加
  - カスタムハッシュタグ機能を追加

### 技術的な変更
- 新規ファイル: `services/youtube_service.py`
- 新規ファイル: `services/hashtag_formatter.py`
- 更新: `services/instagram_service.py` - カスタムハッシュタグ対応（自動#付与）
- 更新: `services/tiktok_service.py` - カスタムハッシュタグ対応（自動#付与）
- 更新: `app.py` - YouTube対応とハッシュタグパラメータ処理

## [2.0.0] - 2026-02-21

### 追加
- ✅ TikTok動画のシェアに対応
- ✅ プラットフォーム自動検出機能

### 変更
- 📝 プロジェクト名を "Instagram Share Webhook" から "Social Media Share Webhook" に変更

## [1.0.0] - 2026-02-20

### 追加
- ✅ Instagram投稿のシェア機能
- ✅ Pushover通知機能
- ✅ X投稿用Intent URL生成
- ✅ Renderデプロイ対応
