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
        # URLを正規化（クエリパラメータを削除）
        clean_url = url.split('?')[0]
        
        # 投稿タイプ判定
        is_reel = '/reel/' in clean_url
        is_story = '/stories/' in clean_url
        
        # 投稿コード抽出
        code_match = re.search(r'/(p|reel)/([A-Za-z0-9_-]+)', clean_url)
        post_code = code_match.group(2) if code_match else ''
        
        print(f"Fetching Instagram info for: {clean_url}")
        print(f"Post code: {post_code}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        response = requests.get(clean_url, headers=headers, timeout=15, allow_redirects=True)
        print(f"Response status: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # OGタグから情報取得
        og_title = soup.find('meta', property='og:title')
        og_description = soup.find('meta', property='og:description')
        og_image = soup.find('meta', property='og:image')
        
        print(f"OG Title: {og_title['content'] if og_title else 'None'}")
        print(f"OG Description: {og_description['content'][:100] if og_description else 'None'}")
        
        # ユーザー名を抽出（複数の方法を試す）
        username = 'Instagram'
        
        # 方法1: OGタイトルから抽出
        if og_title:
            title_text = og_title['content']
            # パターン: "Username on Instagram: ..."
            if ' on Instagram' in title_text:
                username = title_text.split(' on Instagram')[0].strip()
                # "@" を削除
                username = username.lstrip('@')
            # パターン: "Username (@username) • Instagram photos and videos"
            elif '(@' in title_text:
                match = re.search(r'\(@([^)]+)\)', title_text)
                if match:
                    username = match.group(1)
            # パターン: "Username • Instagram photos and videos"
            elif ' • Instagram' in title_text:
                username = title_text.split(' • Instagram')[0].strip()
        
        # 方法2: URLから抽出（フォールバック）
        if username == 'Instagram':
            # /p/CODE/ の前のユーザー名を探す
            # 通常のURL: https://www.instagram.com/username/p/CODE/
            # リールURL: https://www.instagram.com/username/reel/CODE/
            url_match = re.search(r'instagram\.com/([^/]+)/(p|reel)/', clean_url)
            if url_match:
                username = url_match.group(1)
        
        print(f"Extracted username: {username}")
        
        # 説明文を取得
        description = ''
        if og_description:
            desc_text = og_description['content']
            
            # パターン1: "X Likes, Y Comments - Description"
            if ' - ' in desc_text:
                parts = desc_text.split(' - ', 1)
                if len(parts) > 1:
                    description = parts[1].strip()
            # パターン2: "X Followers, Y Following, Z Posts - Description"
            elif 'Followers' in desc_text and ' - ' in desc_text:
                parts = desc_text.split(' - ', 1)
                if len(parts) > 1:
                    description = parts[1].strip()
            # パターン3: そのまま使用
            else:
                description = desc_text.strip()
            
            # 末尾の "See Instagram photos and videos..." を削除
            if 'See Instagram photos and videos' in description:
                description = description.split('See Instagram photos and videos')[0].strip()
        
        # 説明文が空の場合、タイトルから抽出を試みる
        if not description and og_title:
            title_text = og_title['content']
            if ':' in title_text and ' on Instagram' in title_text:
                # "Username on Instagram: Description"
                parts = title_text.split(':', 1)
                if len(parts) > 1:
                    description = parts[1].split(' on Instagram')[0].strip().strip('"')
        
        print(f"Extracted description: {description[:100] if description else 'None'}")
        
        info = {
            'url': clean_url,
            'username': username,
            'post_code': post_code,
            'title': og_title['content'] if og_title else '',
            'description': description if description else f'{username}さんのInstagram投稿',
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
        clean_url = url.split('?')[0]
        
        # URLからユーザー名を抽出
        username = 'Instagram'
        url_match = re.search(r'instagram\.com/([^/]+)/(p|reel)/', clean_url)
        if url_match:
            username = url_match.group(1)
        
        return {
            'url': clean_url,
            'username': username,
            'post_code': '',
            'title': '',
            'description': f'{username}さんのInstagram投稿',
            'image_url': '',
            'is_reel': '/reel/' in clean_url,
            'is_story': '/stories/' in clean_url,
            'type': 'リール' if '/reel/' in clean_url else 'ストーリー' if '/stories/' in clean_url else '投稿'
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
        
        # URLを取得（複数のパターンに対応）
        instagram_url = data.get('url', '')
        
        # パターン1: 二重ネストの辞書
        if isinstance(instagram_url, dict):
            instagram_url = instagram_url.get('url', '')
        
        # パターン2: 文字列化された辞書
        if isinstance(instagram_url, str) and instagram_url.startswith('{'):
            try:
                import json
                parsed = json.loads(instagram_url)
                if isinstance(parsed, dict):
                    instagram_url = parsed.get('url', '')
            except:
                pass
        
        # パターン3: エスケープされたJSON文字列
        if isinstance(instagram_url, str) and '\\/' in instagram_url:
            # バックスラッシュをアンエスケープ
            instagram_url = instagram_url.replace('\\/', '/')
            # もう一度JSONパースを試みる
            if instagram_url.startswith('{'):
                try:
                    import json
                    parsed = json.loads(instagram_url)
                    if isinstance(parsed, dict):
                        instagram_url = parsed.get('url', '')
                except:
                    pass
        
        # デバッグ用ログ
        print(f"Extracted URL type: {type(instagram_url)}")
        print(f"Extracted URL: {instagram_url}")
        
        if not instagram_url:
            return jsonify({'error': 'No URL provided'}), 400
        
        # 最終的にまだ辞書形式の文字列が残っている場合
        if isinstance(instagram_url, str) and instagram_url.startswith('{'):
            return jsonify({'error': f'Invalid URL format: {instagram_url}'}), 400
        
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
