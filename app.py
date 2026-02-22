"""
Social Media Share Webhook Server
iPhoneの共有ボタンから受け取ったSNS URLを処理し、
テンプレート化されたX投稿リンクをPushoverに通知する

対応プラットフォーム:
- Instagram
- TikTok
"""

from flask import Flask, request, jsonify
import requests
import os
from datetime import datetime

# サービスとテンプレートをインポート
from services.common import detect_platform, create_twitter_intent_url
from services.instagram_service import extract_instagram_info
from services.tiktok_service import extract_tiktok_info
from templates import create_tweet_text, create_pushover_message, create_pushover_title

app = Flask(__name__)

# 環境変数から設定を取得
PUSHOVER_TOKEN = os.environ.get('PUSHOVER_TOKEN', '')
PUSHOVER_USER = os.environ.get('PUSHOVER_USER', '')


def extract_social_media_info(url, data):
    """URLからプラットフォームを検出し、適切な情報抽出サービスを呼び出す"""
    
    platform = detect_platform(url)
    
    if not platform:
        raise ValueError(f"Unsupported platform: {url}")
    
    print(f"✓ Detected platform: {platform}")
    
    # 共通パラメータを取得
    provided_username = data.get('username', '').strip()
    provided_caption = data.get('caption', '').strip()
    
    # プラットフォーム別に情報抽出
    if platform == 'instagram':
        return extract_instagram_info(url, provided_username, provided_caption)
    elif platform == 'tiktok':
        return extract_tiktok_info(url, provided_username, provided_caption)
    else:
        raise ValueError(f"Platform not implemented: {platform}")


def send_pushover_notification(info, twitter_url):
    """Pushoverに通知を送信"""
    
    if not PUSHOVER_TOKEN or not PUSHOVER_USER:
        print("Pushover credentials not configured")
        return False
    
    # メッセージとタイトルを生成
    message = create_pushover_message(info)
    title = create_pushover_title(info)
    
    try:
        response = requests.post(
            'https://api.pushover.net/1/messages.json',
            data={
                'token': PUSHOVER_TOKEN,
                'user': PUSHOVER_USER,
                'message': message,
                'title': title,
                'url': twitter_url,
                'url_title': 'Xに投稿する',
                'priority': 0
            },
            timeout=10
        )
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"Error sending Pushover notification: {e}")
        return False


@app.route('/')
def index():
    """ヘルスチェック用エンドポイント"""
    return jsonify({
        'status': 'ok',
        'service': 'Social Media Share Webhook',
        'version': '2.0.0',
        'supported_platforms': ['instagram', 'tiktok'],
        'endpoints': {
            'webhook': '/webhook (POST)',
            'health': '/ (GET)'
        }
    })


@app.route('/webhook', methods=['POST'])
def webhook():
    """SNS URLを受け取って処理"""
    
    try:
        # リクエストデータ取得
        data = request.get_json()
        
        # デバッグ用ログ
        print(f"Received data type: {type(data)}")
        print(f"Received data: {data}")
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # URLを取得（複数のパターンに対応）
        social_url = data.get('url', '')
        
        # パターン1: 二重ネストの辞書
        if isinstance(social_url, dict):
            social_url = social_url.get('url', '')
        
        # パターン2: 文字列化された辞書
        if isinstance(social_url, str) and social_url.startswith('{'):
            try:
                import json
                parsed = json.loads(social_url)
                if isinstance(parsed, dict):
                    social_url = parsed.get('url', '')
            except:
                pass
        
        # パターン3: エスケープされたJSON文字列
        if isinstance(social_url, str) and '\\/' in social_url:
            social_url = social_url.replace('\\/', '/')
            if social_url.startswith('{'):
                try:
                    import json
                    parsed = json.loads(social_url)
                    if isinstance(parsed, dict):
                        social_url = parsed.get('url', '')
                except:
                    pass
        
        # デバッグ用ログ
        print(f"Extracted URL type: {type(social_url)}")
        print(f"Extracted URL: {social_url}")
        
        if not social_url:
            return jsonify({'error': 'No URL provided'}), 400
        
        # 最終的にまだ辞書形式の文字列が残っている場合
        if isinstance(social_url, str) and social_url.startswith('{'):
            return jsonify({'error': f'Invalid URL format: {social_url}'}), 400
        
        # プラットフォーム検出
        platform = detect_platform(social_url)
        if not platform:
            return jsonify({'error': 'Unsupported platform. Supported: Instagram, TikTok'}), 400
        
        print(f"Processing {platform.title()} URL: {social_url}")
        
        # SNS情報取得
        social_info = extract_social_media_info(social_url, data)
        
        # X投稿文生成
        tweet_text = create_tweet_text(social_info)
        
        # X投稿用URL生成
        twitter_url = create_twitter_intent_url(tweet_text)
        
        # Pushover通知送信
        notification_sent = send_pushover_notification(social_info, twitter_url)
        
        return jsonify({
            'status': 'success',
            'platform': platform,
            'info': {
                'url': social_info.url,
                'username': social_info.username,
                'type': social_info.type,
                'platform': social_info.platform
            },
            'tweet_text': tweet_text,
            'twitter_url': twitter_url,
            'notification_sent': notification_sent,
            'timestamp': datetime.now().isoformat()
        })
        
    except ValueError as e:
        print(f"Validation error: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400
        
    except Exception as e:
        print(f"Error processing webhook: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/health')
def health():
    """ヘルスチェック"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
