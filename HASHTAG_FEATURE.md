# カスタムハッシュタグ機能ガイド

## 📝 概要

カスタムハッシュタグ機能を使うと、ユーザー名ベースのハッシュタグに加えて、追加のハッシュタグを指定できます。

## ✨ 特徴

- ユーザー名/チャンネル名が自動的にベースハッシュタグになる
- `hashtags`パラメータで追加のハッシュタグを指定可能
- `#`記号なしで入力（自動的に付与されます）
- スペース区切りで複数指定可能

## 🎯 ハッシュタグの構成

### 基本構造

```
#ユーザー名 #追加タグ1 #追加タグ2 ...
```

### 例

| ユーザー名 | 追加ハッシュタグ | 結果 |
|-----------|----------------|------|
| `member_name` | なし | `#member_name` |
| `member_name` | `STU48 アイドル` | `#member_name #STU48 #アイドル` |
| `artist_name` | `音楽 NewRelease` | `#artist_name #音楽 #NewRelease` |

## 🔧 設定例

### 例1: ユーザー名のみ（追加ハッシュタグなし）

```
辞書:
  url: ショートカット入力
```

結果: `#ユーザー名`

### 例2: ユーザー名 + 追加ハッシュタグ

```
辞書:
  url: ショートカット入力
  hashtags: STU48 アイドル
```

結果: `#ユーザー名 #STU48 #アイドル`

### 例3: ユーザー名を指定 + 追加ハッシュタグ

```
辞書:
  url: ショートカット入力
  username: member_name
  hashtags: STU48 アイドル
```

結果: `#member_name #STU48 #アイドル`

### 例4: プラットフォーム別の追加ハッシュタグ

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

## 📊 実際の投稿例

### 例1: Instagram投稿（追加ハッシュタグなし）

**入力:**
```
URL: https://instagram.com/member_name/p/xxxxx/
```

**生成される投稿文:**
```
📷 member_nameの投稿

今日のライブ楽しかった！

https://instagram.com/p/xxxxx/

#member_name
```

### 例2: Instagram投稿（追加ハッシュタグあり）

**入力:**
```
URL: https://instagram.com/member_name/p/xxxxx/
hashtags: STU48 アイドル
```

**生成される投稿文:**
```
📷 member_nameの投稿

今日のライブ楽しかった！

https://instagram.com/p/xxxxx/

#member_name #STU48 #アイドル
```

### 例3: YouTube動画（ユーザー名指定 + 追加ハッシュタグ）

**入力:**
```
URL: https://youtube.com/watch?v=xxxxx
username: ArtistName
hashtags: 音楽 NewRelease
```

**生成される投稿文:**
```
🎥 ArtistNameの動画

新曲MV公開！

https://youtube.com/watch?v=xxxxx

#ArtistName #音楽 #NewRelease
```

### 例4: TikTok動画（追加ハッシュタグあり）

**入力:**
```
URL: https://tiktok.com/@creator/video/xxxxx
hashtags: バズり動画 面白い
```

**生成される投稿文:**
```
🎵 creatorの動画

面白すぎる！

https://tiktok.com/@creator/video/xxxxx

#creator #バズり動画 #面白い
```

## 🔍 技術的な詳細

### ハッシュタグの生成ロジック

1. ベースハッシュタグを生成（ユーザー名/チャンネル名から）
2. 追加ハッシュタグが指定されている場合は、フォーマットして追加
3. 最終的なハッシュタグ文字列を生成

### ハッシュタグフォーマッター

`services/hashtag_formatter.py` で実装されています。

```python
def format_hashtags(hashtags_input):
    """
    ハッシュタグ文字列をフォーマット
    
    入力: "STU48 アイドル 瀬戸内"
    出力: "#STU48 #アイドル #瀬戸内"
    """
```

### 処理フロー

1. ユーザー名からベースハッシュタグを生成（例: `#member_name`）
2. 追加ハッシュタグが指定されている場合:
   - 入力文字列をスペースで分割
   - 各タグをトリム
   - `#`で始まっていない場合は`#`を付与
   - スペース区切りで結合
3. ベースハッシュタグと追加ハッシュタグを結合

### テスト

`test_hashtag_formatter.py` で10個のテストケースを実行：

```bash
python3 test_hashtag_formatter.py
```

すべてのテストが成功することを確認済み。

## 💡 ヒント

- ユーザー名は自動的にベースハッシュタグになります
- `hashtags`パラメータで追加のハッシュタグを指定
- `#`記号は不要（自動的に付与されます）
- スペース区切りで複数指定
- 既に`#`がある場合も正しく処理
- 日本語と英語の混在も可能
- 絵文字も使用可能

## ⚠️ 注意事項

- ハッシュタグは最大280文字まで
- 投稿本文とURLを含めた全体が280文字を超える場合、本文が自動的に短縮されます
- カンマ区切りは不可（スペース区切りのみ）
- ユーザー名が取得できない場合は、プラットフォーム名がベースハッシュタグになります

## 🐛 トラブルシューティング

### 追加ハッシュタグが反映されない

- ショートカットの辞書に `hashtags` キーが追加されているか確認
- キー名は小文字で `hashtags`（大文字不可）
- 値は `#`記号なしで入力

### ユーザー名がハッシュタグに含まれない

- ユーザー名は自動的に取得されます
- 取得できない場合は、`username`パラメータで指定可能
- 例: `username: member_name`

### 複数のハッシュタグが正しく表示されない

- スペース区切りで入力
- カンマ区切りは不可

### ベースハッシュタグのみにしたい

- `hashtags` キーを省略
- または `hashtags` の値を空にする

## 📚 関連ドキュメント

- [SHORTCUT_SETUP.md](SHORTCUT_SETUP.md) - ショートカット設定ガイド
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - 使い方ガイド
- [UPDATE_SUMMARY_v3.md](UPDATE_SUMMARY_v3.md) - v3.0.0アップデート概要

---

最終更新: 2026年3月12日
