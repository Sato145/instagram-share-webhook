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

## 🏷️ カスタムハッシュタグの使い方

### 方法1: ショートカットに固定ハッシュタグを設定

ショートカットの辞書アクションに `hashtags` キーを追加：

```
辞書:
  url: ショートカット入力
  hashtags: #STU48 #アイドル
```

この設定で、すべての共有に同じハッシュタグが使われます。

### 方法2: プラットフォーム別にハッシュタグを変更

条件分岐を使って、プラットフォームごとに異なるハッシュタグを設定：

```
if URLに「instagram.com」が含まれる
  変数を設定: hashtags = "#Instagram #写真"
それ以外 if URLに「tiktok.com」が含まれる
  変数を設定: hashtags = "#TikTok #動画"
それ以外 if URLに「youtube.com」が含まれる
  変数を設定: hashtags = "#YouTube #動画"

辞書:
  url: ショートカット入力
  hashtags: 変数 hashtags
```

### 方法3: 複数のショートカットを作成

用途別に複数のショートカットを作成：

#### アイドル用
```
名前: アイドル共有
辞書:
  url: ショートカット入力
  hashtags: #STU48 #アイドル
```

#### 音楽用
```
名前: 音楽共有
辞書:
  url: ショートカット入力
  hashtags: #音楽 #Music
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

### 例1: STU48メンバーのInstagram投稿を共有

ショートカット設定：
```
hashtags: #STU48 #アイドル
```

生成される投稿文：
```
📷 member_nameの投稿

今日のライブ楽しかった！

https://instagram.com/p/xxxxx/

#STU48 #アイドル
```

### 例2: 好きなアーティストのYouTube動画を共有

ショートカット設定：
```
hashtags: #音楽 #NewRelease
```

生成される投稿文：
```
🎥 Artist Nameの動画

新曲MV公開！

https://youtube.com/watch?v=xxxxx

#音楽 #NewRelease
```

### 例3: バイラル動画をTikTokから共有

ショートカット設定：
```
hashtags: #TikTok #バズり動画
```

生成される投稿文：
```
🎵 creator_nameの動画

面白すぎる！

https://tiktok.com/@creator/video/xxxxx

#TikTok #バズり動画
```

## 🔧 トラブルシューティング

### ハッシュタグが反映されない

- ショートカットの辞書に `hashtags` キーが正しく追加されているか確認
- キー名は小文字で `hashtags` と入力（大文字不可）
- 値は `#` から始まるハッシュタグ形式

### 複数のハッシュタグが正しく表示されない

- ハッシュタグはスペース区切りで入力
- 例: `#Tag1 #Tag2 #Tag3`
- カンマ区切りは不可

### デフォルトハッシュタグに戻したい

- ショートカットの辞書から `hashtags` キーを削除
- または `hashtags` の値を空にする

## 💡 ヒント

- ハッシュタグは最大280文字（X投稿の制限）まで
- 投稿本文とURLを含めた全体が280文字を超える場合、本文が自動的に短縮されます
- 絵文字もハッシュタグに使用可能（例: `#🎵音楽`）
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
