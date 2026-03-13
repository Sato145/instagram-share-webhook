# 使い方ガイド

## 📱 基本的な使い方

### 1. Instagram投稿を共有

1. Instagramアプリで投稿を開く
2. 共有ボタン（紙飛行機アイコン）をタップ
3. 「SNS共有」ショートカットを選択
4. Pushover通知が届く
5. 通知をタップしてXに投稿

### 2. TikTok動画を共有

1. TikTokアプリで動画を開く
2. 共有ボタンをタップ
3. 「SNS共有」ショートカットを選択
4. Pushover通知が届く
5. 通知をタップしてXに投稿

### 3. YouTube動画を共有

1. YouTubeアプリで動画を開く
2. 共有ボタンをタップ
3. 「SNS共有」ショートカットを選択
4. Pushover通知が届く
5. 通知をタップしてXに投稿

### 4. Xポストを共有

1. Xアプリでポストを開く
2. 共有ボタンをタップ
3. 「SNS共有」ショートカットを選択
4. Pushover通知が届く
5. 通知をタップしてXに投稿

### 5. Threadsスレッドを共有

1. Threadsアプリでスレッドを開く
2. 共有ボタンをタップ
3. 「SNS共有」ショートカットを選択
4. Pushover通知が届く
5. 通知をタップしてXに投稿

### 6. Facebook投稿を共有

1. Facebookアプリで投稿を開く
2. 共有ボタンをタップ
3. 「SNS共有」ショートカットを選択
4. Pushover通知が届く
5. 通知をタップしてXに投稿

### 7. LinkedIn投稿を共有

1. LinkedInアプリで投稿を開く
2. 共有ボタンをタップ
3. 「SNS共有」ショートカットを選択
4. Pushover通知が届く
5. 通知をタップしてXに投稿

## 🏷️ カスタムハッシュタグの使い方

### ハッシュタグの構成

ハッシュタグは以下の構成になります：

```
#ユーザー名 #追加タグ1 #追加タグ2 ...
```

- ユーザー名/チャンネル名が自動的にベースハッシュタグになります
- `hashtags`パラメータで追加のハッシュタグを指定できます

### 方法1: ユーザー名のみ（デフォルト）

```
辞書:
  url: ショートカット入力
```

結果: `#ユーザー名`

### 方法2: ユーザー名 + 追加ハッシュタグ

ショートカットの辞書アクションに `hashtags` キーを追加：

```
辞書:
  url: ショートカット入力
  hashtags: STU48 アイドル
```

⚠️ 重要: `#`記号は不要です。自動的に付与されます。

結果: `#ユーザー名 #STU48 #アイドル`

### 方法3: ユーザー名を指定 + 追加ハッシュタグ

```
辞書:
  url: ショートカット入力
  username: member_name
  hashtags: STU48 アイドル
```

結果: `#member_name #STU48 #アイドル`

### 方法4: プラットフォーム別に追加ハッシュタグを変更

条件分岐を使って、プラットフォームごとに異なる追加ハッシュタグを設定：

```
if URLに「instagram.com」が含まれる
  変数を設定: hashtags = "写真 Instagram"
それ以外 if URLに「tiktok.com」が含まれる
  変数を設定: hashtags = "動画 TikTok"
それ以外 if URLに「youtube.com」が含まれる
  変数を設定: hashtags = "動画 YouTube"

辞書:
  url: ショートカット入力
  hashtags: 変数 hashtags
```

### 方法5: 複数のショートカットを作成

用途別に複数のショートカットを作成：

#### アイドル用
```
名前: アイドル共有
辞書:
  url: ショートカット入力
  hashtags: STU48 アイドル
```

#### 音楽用
```
名前: 音楽共有
辞書:
  url: ショートカット入力
  hashtags: 音楽 Music
```

## 📝 投稿文のフォーマット

### デフォルト（ハッシュタグなし）

```
🎬 ユーザー名のリール

投稿本文（最大100文字）

https://instagram.com/p/xxxxx/

#ユーザー名
```

### カスタムハッシュタグあり

```
🎬 ユーザー名のリール

投稿本文（最大100文字）

https://instagram.com/p/xxxxx/

#STU48 #アイドル
```

## 🎯 使用例

### 例1: STU48メンバーのInstagram投稿を共有（追加ハッシュタグあり）

ショートカット設定：
```
hashtags: STU48 アイドル
```

生成される投稿文：
```
📷 member_nameの投稿

今日のライブ楽しかった！

https://instagram.com/p/xxxxx/

#member_name #STU48 #アイドル
```

### 例2: 好きなアーティストのYouTube動画を共有

ショートカット設定：
```
username: ArtistName
hashtags: 音楽 NewRelease
```

生成される投稿文：
```
🎥 ArtistNameの動画

新曲MV公開！

https://youtube.com/watch?v=xxxxx

#ArtistName #音楽 #NewRelease
```

### 例3: バイラル動画をTikTokから共有（ユーザー名のみ）

ショートカット設定：
```
（hashtagsなし）
```

生成される投稿文：
```
🎵 creator_nameの動画

面白すぎる！

https://tiktok.com/@creator/video/xxxxx

#creator_name
```

## 🔧 トラブルシューティング

### ハッシュタグが反映されない

- ショートカットの辞書に `hashtags` キーが正しく追加されているか確認
- キー名は小文字で `hashtags` と入力（大文字不可）
- 値は `#`記号なしで入力（例: `STU48 アイドル`）

### ユーザー名がハッシュタグに含まれない

- ユーザー名は自動的に取得されます
- 取得できない場合は、`username`パラメータで指定可能
- 例: `username: member_name`

### 複数のハッシュタグが正しく表示されない

- ハッシュタグはスペース区切りで入力
- 例: `STU48 アイドル 瀬戸内`
- `#`記号は不要（自動的に付与されます）
- カンマ区切りは不可

### ユーザー名のみのハッシュタグにしたい

- ショートカットの辞書から `hashtags` キーを削除
- または `hashtags` の値を空にする

## 💡 ヒント

- ユーザー名は自動的にベースハッシュタグになります
- `hashtags`パラメータで追加のハッシュタグを指定
- ハッシュタグは `#`記号なしで入力（自動的に付与されます）
- ハッシュタグは最大280文字（X投稿の制限）まで
- 投稿本文とURLを含めた全体が280文字を超える場合、本文が自動的に短縮されます
- 絵文字もハッシュタグに使用可能（例: `🎵音楽`）
- 日本語ハッシュタグも使用可能

## 📊 対応URL形式

### Instagram
- 投稿: `https://www.instagram.com/p/xxxxx/`
- リール: `https://www.instagram.com/reel/xxxxx/`
- ストーリー: `https://www.instagram.com/stories/username/xxxxx/`

### TikTok
- 通常: `https://www.tiktok.com/@username/video/xxxxx`
- 短縮: `https://vt.tiktok.com/xxxxx/`

### YouTube
- 通常: `https://www.youtube.com/watch?v=xxxxx`
- 短縮: `https://youtu.be/xxxxx`
- Shorts: `https://www.youtube.com/shorts/xxxxx`

### X (Twitter)
- 通常: `https://twitter.com/username/status/xxxxx`
- 新ドメイン: `https://x.com/username/status/xxxxx`

### Threads
- スレッド: `https://www.threads.net/@username/post/xxxxx`

### Facebook
- 投稿: `https://www.facebook.com/username/posts/xxxxx`
- 動画: `https://www.facebook.com/username/videos/xxxxx`

### LinkedIn
- 投稿: `https://www.linkedin.com/posts/username_xxxxx`
- フィード: `https://www.linkedin.com/feed/update/urn:li:activity:xxxxx`
