"""
YouTube機能のテストスクリプト
"""

import requests
import json

# テスト用のYouTube URL
test_urls = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://youtu.be/dQw4w9WgXcQ",
    "https://www.youtube.com/shorts/abc123def45",
]

# Webhookエンドポイント
WEBHOOK_URL = "http://localhost:5000/webhook"

def test_youtube_url(url, hashtags=None):
    """YouTube URLをテスト"""
    print(f"\n{'='*60}")
    print(f"Testing: {url}")
    print(f"{'='*60}")
    
    payload = {
        "url": url
    }
    
    if hashtags:
        payload["hashtags"] = hashtags
        print(f"Custom hashtags: {hashtags} (will be formatted to add #)")
    
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
    print("YouTube Webhook Test")
    print("=" * 60)
    
    # 基本テスト
    test_youtube_url(test_urls[0])
    
    # カスタムハッシュタグテスト（#記号なし）
    test_youtube_url(test_urls[0], hashtags="YouTube 音楽")
