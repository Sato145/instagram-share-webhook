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
        clean_url = url.split('?')[0].rstrip('/')
        
        print(f"Processing URL: {clean_url}")
        
        # 投稿タイプ判定
        is_reel = '/reel/' in clean_url
        is_story = '/stories/' in clean_url
        
        # 投稿コード抽出
        code_match = re.search(r'/(p|reel)/([A-Za-z0-9_-]+)', clean_url)
        post_code = code_match.group(2) if code_match else ''
        
        # URLからユーザー名を抽出（複数パターン対応）
        username = None
        
        # パターン1: https://www.instagram.com/username/p/CODE/ または /reel/CODE/
        url_match = re.search(r'instagram\.com/([^/]+)/(p|reel)/', clean_url)
        if url_match:
            potential_username = url_match.group(1)
            # 'www', 'p', 'reel', 'stories' などは除外
            if potential_username not in ['www', 'p', 'reel', 'stories', 'tv']:
                username = potential_username
                print(f"✓ Extracted username from URL pattern 1: {username}")
        
        # パターン2: https://www.instagram.com/reel/CODE/ (ユーザー名なし、OGタグから取得必要)
        if not username:
            print(f"⚠ Could not extract username from URL, will try OG tags")
        
        print(f"Post code: {post_code}")
        print(f"Is reel: {is_reel}")
        
        # Instagram情報を取得（複数の方法を試行）
        description = ''
        
        # 方法1: oEmbed API（公式の埋め込み用API）
        try:
            oembed_url = f"https://graph.facebook.com/v12.0/instagram_oembed?url={clean_url}&access_token=&omitscript=true"
            oembed_response = requests.get(oembed_url, timeout=10)
            
            if oembed_response.status_code == 200:
                oembed_data = oembed_response.json()
                print(f"oEmbed data: {oembed_data}")
                
                # ユーザー名を抽出
                if 'author_name' in oembed_data and not username:
                    username = oembed_data['author_name'].lstrip('@')
                    print(f"✓ Extracted username from oEmbed: {username}")
                
                # タイトルから説明文を抽出
                if 'title' in oembed_data:
                    title = oembed_data['title']
                    # "Username on Instagram: "投稿内容""
                    if ' on Instagram:' in title:
                        description = title.split(' on Instagram:', 1)[1].strip().strip('"').strip('"')
                        print(f"✓ Extracted description from oEmbed: {description[:100]}")
        except Exception as e:
            print(f"oEmbed API failed: {e}")
        
        # 方法2: HTMLページから取得（フォールバック）
        if not username or not description:
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Cache-Control': 'max-age=0'
                }
                
                response = requests.get(clean_url, headers=headers, timeout=15, allow_redirects=True)
                print(f"Response status: {response.status_code}")
                print(f"Response URL: {response.url}")
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # すべてのmetaタグをログ出力（デバッグ用）
                    all_metas = soup.find_all('meta')
                    print(f"Found {len(all_metas)} meta tags")
                    
                    # OGタグから情報取得
                    og_title = soup.find('meta', property='og:title')
                    og_description = soup.find('meta', property='og:description')
                    
                    # Twitterカードも試す
                    twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
                    twitter_description = soup.find('meta', attrs={'name': 'twitter:description'})
                    
                    # タイトルからユーザー名を抽出
                    title_tag = og_title or twitter_title
                    if title_tag and 'content' in title_tag.attrs:
                        title_text = title_tag['content']
                        print(f"OG/Twitter Title: {title_text}")
                        
                        # ユーザー名抽出パターン
                        # "Username on Instagram: "投稿内容""
                        # "Username (@username) • Instagram photos and videos"
                        # "@username on Instagram: "投稿内容""
                        
                        if not username:  # URLから取得できなかった場合のみ
                            # パターン1: "Username on Instagram"
                            if ' on Instagram' in title_text:
                                username_from_title = title_text.split(' on Instagram')[0].strip()
                                if username_from_title and username_from_title not in ['Instagram', '']:
                                    username = username_from_title.lstrip('@')
                                    print(f"✓ Extracted username from OG title (pattern 1): {username}")
                            
                            # パターン2: "Username (@username)"
                            elif '(@' in title_text:
                                match = re.search(r'\(@([^)]+)\)', title_text)
                                if match:
                                    username = match.group(1)
                                    print(f"✓ Extracted username from OG title (pattern 2): {username}")
                            
                            # パターン3: "@username" で始まる
                            elif title_text.startswith('@'):
                                username_from_title = title_text.split()[0].lstrip('@')
                                if username_from_title:
                                    username = username_from_title
                                    print(f"✓ Extracted username from OG title (pattern 3): {username}")
                    
                    # 説明文を抽出
                    if not description:  # oEmbedで取得できなかった場合のみ
                        desc_tag = og_description or twitter_description
                        if desc_tag and 'content' in desc_tag.attrs:
                            desc_text = desc_tag['content']
                            print(f"OG/Twitter Description: {desc_text[:150]}")
                            
                            # 説明文のクリーニング
                            # "123 likes, 45 comments - username on Instagram: "投稿内容""
                            if ' - ' in desc_text and ' on Instagram:' in desc_text:
                                # "username on Instagram: "投稿内容"" の部分を抽出
                                parts = desc_text.split(' on Instagram:', 1)
                                if len(parts) == 2:
                                    # ユーザー名も抽出（まだ取得できていない場合）
                                    if not username:
                                        username_part = parts[0].split(' - ')[-1].strip()
                                        if username_part and username_part not in ['Instagram', '']:
                                            username = username_part.lstrip('@')
                                            print(f"✓ Extracted username from description: {username}")
                                    
                                    # 投稿内容を抽出
                                    description = parts[1].strip().strip('"').strip('"')
                            elif desc_text and not desc_text.startswith('See Instagram'):
                                description = desc_text.strip()
                            
                            # 不要な文字列を削除
                            unwanted_phrases = [
                                'See Instagram photos and videos',
                                'See photos, videos and more on Instagram',
                                'View this post on Instagram'
                            ]
                            for phrase in unwanted_phrases:
                                if phrase in description:
                                    description = description.split(phrase)[0].strip()
                    
                    print(f"Extracted description: {description[:100] if description else 'None'}")
        
        except Exception as e:
            print(f"Error fetching OG tags: {e}")
            import traceback
            traceback.print_exc()
        
        # ユーザー名が取得できなかった場合のフォールバック
        if not username:
            username = 'Instagram'
            print(f"⚠ Using fallback username: {username}")
        
        # 説明文が取得できなかった場合のデフォルト
        if not description:
            if username != 'Instagram':
                description = f'{username}さんの{"リール" if is_reel else "投稿"}をチェック！'
            else:
                description = 'Instagram投稿をチェック！'
        
        print(f"✓ Final username: {username}")
        print(f"✓ Final description: {description[:100]}")
        
        info = {
            'url': clean_url,
            'username': username,
            'post_code': post_code,
            'title': '',
            'description': description,
            'image_url': '',
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
        clean_url = url.split('?')[0].rstrip('/')
        
        # URLからユーザー名を抽出
        username = 'Instagram'
        url_match = re.search(r'instagram\.com/([^/]+)/(p|reel)/', clean_url)
        if url_match:
            potential_username = url_match.group(1)
            if potential_username not in ['www', 'p', 'reel', 'stories', 'tv']:
                username = potential_username
        
        is_reel = '/reel/' in clean_url
        
        return {
            'url': clean_url,
            'username': username,
            'post_code': '',
            'title': '',
            'description': f'{username}さんの{"リール" if is_reel else "投稿"}をチェック！',
            'image_url': '',
            'is_reel': is_reel,
            'is_story': '/stories/' in clean_url,
            'type': 'リール' if is_reel else 'ストーリー' if '/stories/' in clean_url else '投稿'
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
