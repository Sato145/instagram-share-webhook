"""
ハッシュタグフォーマッターのテスト
"""

from services.hashtag_formatter import format_hashtags


def test_format_hashtags():
    """ハッシュタグフォーマッターのテスト"""
    
    print("ハッシュタグフォーマッターのテスト")
    print("=" * 60)
    
    # テストケース
    test_cases = [
        # (入力, 期待される出力, 説明)
        ("STU48 アイドル", "#STU48 #アイドル", "基本的な使い方"),
        ("STU48", "#STU48", "単一タグ"),
        ("STU48 アイドル 瀬戸内", "#STU48 #アイドル #瀬戸内", "3つのタグ"),
        ("#STU48 #アイドル", "#STU48 #アイドル", "既に#がある場合"),
        ("STU48 #アイドル", "#STU48 #アイドル", "混在している場合"),
        ("  STU48   アイドル  ", "#STU48 #アイドル", "余分なスペース"),
        ("", "", "空文字列"),
        ("   ", "", "スペースのみ"),
        ("音楽 Music", "#音楽 #Music", "日本語と英語"),
        ("YouTube 動画", "#YouTube #動画", "大文字小文字混在"),
    ]
    
    passed = 0
    failed = 0
    
    for input_str, expected, description in test_cases:
        result = format_hashtags(input_str)
        status = "✓" if result == expected else "✗"
        
        if result == expected:
            passed += 1
        else:
            failed += 1
        
        print(f"\n{status} {description}")
        print(f"  入力: '{input_str}'")
        print(f"  期待: '{expected}'")
        print(f"  結果: '{result}'")
    
    print("\n" + "=" * 60)
    print(f"テスト結果: {passed}件成功, {failed}件失敗")
    
    if failed == 0:
        print("✓ すべてのテストが成功しました！")
    else:
        print(f"✗ {failed}件のテストが失敗しました")
    
    return failed == 0


if __name__ == "__main__":
    success = test_format_hashtags()
    exit(0 if success else 1)
