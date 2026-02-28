"""
Instagram情報抽出サービス
"""

import re
import requests
from bs4 import BeautifulSoup
from . import SocialMediaInfo
from .common import clean_url


def extract_instagram_info(url, provided_username='', provided_caption=''):
    """Instagram URLから投稿情報を取得"""
    
    info = SocialMediaInfo()
    info.platform = 'instagram'
    
    try:
        # URLを正規化
        info.url = clean_url(url)
        
        print(f"Processing Instagram URL: {info.url}")
        
        # 投稿タイプ判定
        is_reel = '/reel/' in info.url
        is_story = '/stories/' in info.url
        
        info.is_video = is_reel
        info.type = 'リール' if is_reel else 'ストーリー' if is_story else '投稿'
        info.emoji = '🎬' if is_reel else '📷'
        
        # 投稿コード抽出
        code_match = re.search(r'/(p|reel)/([A-Za-z0-9_-]+)', info.url)
        info.post_code = code_match.group(2) if code_match else ''
        
        # ユーザー名を抽出（URLから）
        username = None
        url_match = re.search(r'instagram\.com/([^/]+)/(p|reel)/', info.url)
        if url_match:
            potential_username = url_match.group(1)
            if potential_username not in ['www', 'p', 'reel', 'stories', 'tv']:
                username = potential_username
                print(f"✓ Extracted username from URL: {username}")
        
        # 提供されたユーザー名を優先
        if provided_username:
            info.username = provided_username
            print(f"✓ Using provided username: {provided_username}")
        elif username:
            info.username = username
        else:
            info.username = 'Instagram'
            print(f"⚠ Using fallback username: Instagram")
        
        # 提供された投稿本文を優先
        if provided_caption:
            info.description = provided_caption
            print(f"✓ Using provided caption: {provided_caption[:100]}")
        else:
            # OGタグから取得を試みる
            description = _fetch_og_description(info.url)
            if description:
                info.description = description
            else:
                info.description = f'{info.username}の{info.type}をチェック！'
        
        # ハッシュタグを生成
        if info.username == 'Instagram':
            info.hashtag = '#Instagram'
        else:
            clean_username = info.username.replace(' ', '').replace('@', '')
            info.hashtag = f'#{clean_username}'
        
        print(f"✓ Final username: {info.username}")
        print(f"✓ Final description: {info.description[:100]}")
        
        return info
        
    except Exception as e:
        print(f"Error extracting Instagram info: {e}")
        import traceback
        traceback.print_exc()
        
        # フォールバック
        info.url = clean_url(url)
        info.username = provided_username or 'Instagram'
        info.description = provided_caption or 'Instagram投稿をチェック！'
        info.type = 'リール' if '/reel/' in url else '投稿'
        info.emoji = '🎬' if '/reel/' in url else '📷'
        info.hashtag = '#Instagram'
        
        return info


def _fetch_og_description(url):
    """OGタグから説明文を取得（ベストエフォート）"""
    try:
        # 方法1: oEmbed API
        oembed_url = f"https://graph.facebook.com/v12.0/instagram_oembed?url={url}&access_token=&omitscript=true"
        oembed_response = requests.get(oembed_url, timeout=10)
        
        if oembed_response.status_code == 200:
            oembed_data = oembed_response.json()
            if 'title' in oembed_data and ' on Instagram:' in oembed_data['title']:
                description = oembed_data['title'].split(' on Instagram:', 1)[1].strip().strip('"').strip('"')
                if description:
                    print(f"✓ Extracted description from oEmbed: {description[:100]}")
                    return description
    except Exception as e:
        print(f"oEmbed API failed: {e}")
    
    # 方法2: HTMLページから取得
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8',
        }
        
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # OGタグから取得
            og_description = soup.find('meta', property='og:description')
            if og_description and 'content' in og_description.attrs:
                desc_text = og_description['content']
                
                # クリーニング
                if ' - ' in desc_text and ' on Instagram:' in desc_text:
                    parts = desc_text.split(' on Instagram:', 1)
                    if len(parts) == 2:
                        description = parts[1].strip().strip('"').strip('"')
                        if description:
                            print(f"✓ Extracted description from OG tag: {description[:100]}")
                            return description
    except Exception as e:
        print(f"HTML fetch failed: {e}")
    
    return ''
