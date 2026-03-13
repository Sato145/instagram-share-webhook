"""
全プラットフォームのテストスクリプト
"""

import requests
import json

# テスト用のURL
test_urls = {
    'instagram': 'https://www.instagram.com/p/C3xXxXxXxXx/',
    'tiktok': 'https://www.tiktok.com/@username/video/1234567890',
    'youtube': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    'x': 'https://twitter.com/username/status/1234567890',
    'threads': 'https://www.threads.net/@username/post/xxxxx',
    'facebook': 'https://www.facebook.com/username/posts/1234567890',
    'linkedin': 'https://www.linkedin.com/posts/username_xxxxx',
}

# Webhookエンドポイント
WEBHOOK_URL = "http://localhost:5000/webhook"

def test_platform(platform, url, hashtags=None):
    """プラットフォームをテスト"""
    print(f"\n{'='*60}")
    print(f"Testing {platform.upper()}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    
    payload = {
        "url": url
    }
    
    if hashtags:
        payload["hashtags"] = hashtags
        print(f"Custom hashtags: {hashtags}")
    
    try:
        response = requests.post(
            WEBHOOK_URL,
            json=payload,
            timeout=30
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"\nResponse:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("All Platforms Webhook Test")
    print("=" * 60)
    
    # 各プラットフォームをテスト
    for platform, url in test_urls.items():
        test_platform(platform, url)
    
    # カスタムハッシュタグテスト
    print(f"\n{'='*60}")
    print("Testing with custom hashtags")
    print(f"{'='*60}")
    test_platform('instagram', test_urls['instagram'], hashtags="STU48 アイドル")
