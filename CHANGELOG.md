# 変更履歴

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
