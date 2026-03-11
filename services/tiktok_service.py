"""
TikTok情報抽出サービス
"""

import re
import requests
from bs4 import BeautifulSoup
from . import SocialMediaInfo
from .common import clean_url


def extract_tiktok_info(url, provided_username='', provided_caption='', provided_hashtags=''):
    """TikTok URLから投稿情報を取得"""
    
    info = SocialMediaInfo()
    info.platform = 'tiktok'
    info.type = '動画'
    info.is_video = True
    info.emoji = '🎵'
    
    try:
        # 短縮URLの場合は展開
        if 'vt.tiktok.com' in url or 'vm.tiktok.com' in url:
            print(f"Expanding short URL: {url}")
            expanded_url = _expand_short_url(url)
            if expanded_url:
                url = expanded_url
                print(f"✓ Expanded to: {url}")
        
        # URLを正規化
        info.url = clean_url(url)
        
        print(f"Processing TikTok URL: {info.url}")
        
        # ユーザー名を抽出（URLから）
        # パターン: https://www.tiktok.com/@username/video/1234567890
        username = None
        url_match = re.search(r'tiktok\.com/@([^/]+)', info.url)
        if url_match:
            username = url_match.group(1)
            print(f"✓ Extracted username from URL: {username}")
        
        # 動画IDを抽出
        video_match = re.search(r'/video/(\d+)', info.url)
        if video_match:
            info.post_code = video_match.group(1)
            print(f"✓ Extracted video ID: {info.post_code}")
        
        # 提供されたユーザー名を優先
        if provided_username:
            info.username = provided_username.lstrip('@')
            print(f"✓ Using provided username: {info.username}")
        elif username:
            info.username = username
        else:
            info.username = 'TikTok'
            print(f"⚠ Using fallback username: TikTok")
        
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
                info.description = f'{info.username}のTikTok動画をチェック！'
        
        # ハッシュタグを生成
        if provided_hashtags:
            # カスタムハッシュタグが提供されている場合
            info.hashtag = provided_hashtags
            print(f"✓ Using provided hashtags: {provided_hashtags}")
        else:
            # デフォルトハッシュタグ
            if info.username == 'TikTok':
                info.hashtag = '#TikTok'
            else:
                clean_username = info.username.replace(' ', '').replace('@', '')
                info.hashtag = f'#{clean_username}'
        
        print(f"✓ Final username: {info.username}")
        print(f"✓ Final description: {info.description[:100]}")
        print(f"✓ Final hashtag: {info.hashtag}")
        
        return info
        
    except Exception as e:
        print(f"Error extracting TikTok info: {e}")
        import traceback
        traceback.print_exc()
        
        # フォールバック
        info.url = clean_url(url)
        info.username = provided_username.lstrip('@') if provided_username else 'TikTok'
        info.description = provided_caption or 'TikTok動画をチェック！'
        info.hashtag = provided_hashtags or '#TikTok'
        
        return info


def _expand_short_url(short_url):
    """TikTok短縮URLを展開"""
    try:
        response = requests.head(short_url, allow_redirects=True, timeout=10)
        return response.url
    except Exception as e:
        print(f"Failed to expand short URL: {e}")
        return None


def _fetch_og_description(url):
    """OGタグから説明文を取得（ベストエフォート）"""
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
                
                # TikTokの説明文をクリーニング
                # 不要な文字列を削除
                unwanted_phrases = [
                    'Watch more videos',
                    'Download the app',
                    'TikTok video from',
                ]
                for phrase in unwanted_phrases:
                    if phrase in desc_text:
                        desc_text = desc_text.split(phrase)[0].strip()
                
                if desc_text:
                    print(f"✓ Extracted description from OG tag: {desc_text[:100]}")
                    return desc_text
    except Exception as e:
        print(f"HTML fetch failed: {e}")
    
    return ''
