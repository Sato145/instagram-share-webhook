"""
Threads情報抽出サービス
"""

import re
import requests
from bs4 import BeautifulSoup
from . import SocialMediaInfo
from .common import clean_url
from .hashtag_formatter import format_hashtags


def extract_threads_info(url, provided_username='', provided_caption='', provided_hashtags=''):
    """Threads URLから投稿情報を取得"""
    
    info = SocialMediaInfo()
    info.platform = 'threads'
    info.type = 'スレッド'
    info.emoji = '🧵'
    
    try:
        # URLを正規化
        info.url = clean_url(url)
        
        print(f"Processing Threads URL: {info.url}")
        
        # ユーザー名を抽出（URLから）
        # パターン: https://www.threads.net/@username/post/xxxxx
        username = None
        url_match = re.search(r'threads\.net/@([^/]+)', info.url)
        if url_match:
            username = url_match.group(1)
            print(f"✓ Extracted username from URL: {username}")
        
        # ポストIDを抽出
        post_match = re.search(r'/post/([A-Za-z0-9_-]+)', info.url)
        if post_match:
            info.post_code = post_match.group(1)
            print(f"✓ Extracted post ID: {info.post_code}")
        
        # 提供されたユーザー名を優先
        if provided_username:
            info.username = provided_username.lstrip('@')
            print(f"✓ Using provided username: {info.username}")
        elif username:
            info.username = username
        else:
            info.username = 'Threads'
            print(f"⚠ Using fallback username: Threads")
        
        # 提供された投稿本文を優先
        if provided_caption:
            info.description = provided_caption
            print(f"✓ Using provided caption: {provided_caption[:100]}")
        else:
            info.description = f'{info.username}のスレッドをチェック！'
        
        # ハッシュタグを生成
        # ベースハッシュタグ（ユーザー名から）
        if info.username == 'Threads':
            base_hashtag = '#Threads'
        else:
            clean_username = info.username.replace(' ', '').replace('@', '')
            base_hashtag = f'#{clean_username}'
        
        # カスタムハッシュタグが提供されている場合は追加
        if provided_hashtags:
            additional_hashtags = format_hashtags(provided_hashtags)
            info.hashtag = f'{base_hashtag} {additional_hashtags}'
            print(f"✓ Using base hashtag: {base_hashtag}")
            print(f"✓ Adding custom hashtags: {additional_hashtags}")
        else:
            info.hashtag = base_hashtag
        
        print(f"✓ Final username: {info.username}")
        print(f"✓ Final description: {info.description[:100]}")
        print(f"✓ Final hashtag: {info.hashtag}")
        
        return info
        
    except Exception as e:
        print(f"Error extracting Threads info: {e}")
        import traceback
        traceback.print_exc()
        
        # フォールバック
        info.url = clean_url(url)
        info.username = provided_username.lstrip('@') if provided_username else 'Threads'
        info.description = provided_caption or 'Threadsスレッドをチェック！'
        
        # ハッシュタグ生成
        base_hashtag = f'#{info.username}' if info.username != 'Threads' else '#Threads'
        if provided_hashtags:
            additional_hashtags = format_hashtags(provided_hashtags)
            info.hashtag = f'{base_hashtag} {additional_hashtags}'
        else:
            info.hashtag = base_hashtag
        
        return info
