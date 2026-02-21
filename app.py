"""
Instagram Share Webhook Server
iPhoneの共有ボタンから受け取ったInstagram URLを処理し、
テンプレート化されたX投稿リンクをPushoverに通知する
"""

from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
import os
from datetime import datetime
from urllib.parse import quote

app = Flask(__name__)

# 環境変数から設定を取得
PUSHOVER_TOKEN = os.environ.get('PUSHOVER_TOKEN', '')
PUSHOVER_USER = os.environ.get('PUSHOVER_USER', '')

def extract_instagram_info(url):
    """Instagram URLから投稿情報を取得（改善版）"""
    try:
        # 投稿タイプ判定
        is_reel = '/reel/' in url
        is_story = '/stories/' in url
        
        # ユーザー名抽出（URLから）
        username_match = re.search(r'instagram\.com/([^/]+)/', url)
        username = username_match.group(1) if username_match else 'unknown'
        
        # 投稿コード抽出
        code_match = re.search(r'/(p|reel)/([^/]+)/', url)
        post_code = code_match.group(2) if code_match else ''
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # OGタグから情報取得
        og_title = soup.find('meta', property='og:title')
        og_description = soup.find('meta', property='og:description')
        og_image = soup.find('meta', property='og:image')
        
        # タイトルからユーザー名を抽出（OGタグから）
        title_text = og_title['content'] if og_title else ''
        if title_text and ' on Instagram:' in title_text:
            username_from_title = title_text.split(' on Instagram:')[0].strip()
            if username_from_title:
                username = username_from_title
        
        # 説明文を取得
        description = ''
        if og_description:
            desc_text = og_description['content']
            # "X Likes, Y Comments - ..." の形式から本文を抽出
            if ' - ' in desc_text:
                description = desc_text.split(' - ', 1)[1].strip()
            else:
                description = desc_text
        
        # 説明文が空の場合、タイトルから抽出を試みる
        if not description and title_text and ':' in title_text:
            parts = title_text.split(':', 1)
            if len(parts) > 1:
                description = parts[1].strip().strip('"')
        
        info = {
            'url': url,
            'username': username,
            'post_code': post_code,
            'title': title_text,
            'description': description if description else 'Instagram投稿',
            'image_url': og_image['content'] if og_image else '',
            'is_reel': is_reel,
            'is_story': is_story,
            'type': 'リール' if is_reel else 'ストーリー' if is_story else '投稿'
        }
        
        return info
        
    except Exception as e:
        print(f"Error extracting Instagram info: {e}")
        import traceback
        traceback.print_exc()
        
        # フォールバック: URLから最小限の情報を抽出
        username_match = re.search(r'instagram\.com/([^/]+)/', url)
        username = username_match.group(1) if username_match else 'Instagram'
        
        return {
            'url': url,
            'username': username,
            'post_code': '',
            'title': '',
            'description': f'{username}さんのInstagram投稿',
            'image_url': '',
            'is_reel': '/reel/' in url,
            'is_story': '/stories/' in url,
            'type': 'リール' if '/reel/' in url else 'ストーリー' if '/stories/' in url else '投稿'
        }

def create_tweet_text(info):
    """テンプレートに基づいてX投稿文を生成"""
    
    # 投稿タイプに応じた絵文字
    emoji = '🎬' if info['is_reel'] else '📷'
    
    # 本文を短縮（100文字まで）
    description = info['description']
    if len(description) > 100:
        description = description[:100] + '...'
    
    # テンプレート適用
    if description and description != 'Instagram投稿':
        tweet_text = f"{emoji} {info['username']}さんの{info['type']}\n\n{description}\n\n{info['url']}\n\n#Instagram"
    else:
        tweet_text = f"{emoji} {info['username']}さんの{info['type']}\n\n{info['url']}\n\n#Instagram"
    
    return tweet_text

def create_twitter_intent_url(tweet_text):
    """X投稿用のIntent URLを生成"""
    encoded_text = quote(tweet_text)
    return f"https://twitter.com/intent/tweet?text={encoded_text}"

def send_pushover_notification(tweet_text, twitter_url, instagram_info):
    """Pushoverに通知を送信"""
    
    if not PUSHOVER_TOKEN or not PUSHOVER_USER:
        print("Pushover credentials not configured")
        return False
    
    # 通知メッセージ
    message = f"📱 Instagram投稿を共有しました\n\n{tweet_text}\n\n👇 タップしてXに投稿"
    
    try:
        response = requests.post(
            'https://api.pushover.net/1/messages.json',
            data={
                'token': PUSHOVER_TOKEN,
                'user': PUSHOVER_USER,
                'message': message,
                'title': f'Instagram {instagram_info["type"]}を共有',
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
        'service': 'Instagram Share Webhook',
        'version': '1.0.0',
        'endpoints': {
            'webhook': '/webhook (POST)',
            'health': '/ (GET)'
        }
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Instagram URLを受け取って処理"""
    
    try:
        # リクエストデータ取得
        data = request.get_json()
        
        # デバッグ用ログ
        print(f"Received data type: {type(data)}")
        print(f"Received data: {data}")
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        instagram_url = data.get('url', '')
        
        # デバッグ用ログ
        print(f"Extracted URL type: {type(instagram_url)}")
        print(f"Extracted URL: {instagram_url}")
        
        if not instagram_url:
            return jsonify({'error': 'No URL provided'}), 400
        
        # Instagram URLの検証
        if 'instagram.com' not in instagram_url:
            return jsonify({'error': 'Invalid Instagram URL'}), 400
        
        print(f"Processing Instagram URL: {instagram_url}")
        
        # Instagram情報取得
        instagram_info = extract_instagram_info(instagram_url)
        
        # X投稿文生成
        tweet_text = create_tweet_text(instagram_info)
        
        # X投稿用URL生成
        twitter_url = create_twitter_intent_url(tweet_text)
        
        # Pushover通知送信
        notification_sent = send_pushover_notification(
            tweet_text,
            twitter_url,
            instagram_info
        )
        
        return jsonify({
            'status': 'success',
            'instagram_info': {
                'url': instagram_info['url'],
                'username': instagram_info['username'],
                'type': instagram_info['type']
            },
            'tweet_text': tweet_text,
            'twitter_url': twitter_url,
            'notification_sent': notification_sent,
            'timestamp': datetime.now().isoformat()
        })
        
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
