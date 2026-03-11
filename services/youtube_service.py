"""
YouTube情報抽出サービス
"""

import re
import requests
from bs4 import BeautifulSoup
from . import SocialMediaInfo
from .common import clean_url
from .hashtag_formatter import format_hashtags


def extract_youtube_info(url, provided_username='', provided_caption='', provided_hashtags=''):
    """YouTube URLから動画情報を取得"""
    
    info = SocialMediaInfo()
    info.platform = 'youtube'
    info.is_video = True
    info.type = '動画'
    info.emoji = '🎥'
    
    try:
        # URLを正規化
        info.url = _normalize_youtube_url(url)
        
        print(f"Processing YouTube URL: {info.url}")
        
        # 動画IDを抽出
        video_id = _extract_video_id(info.url)
        info.post_code = video_id
        
        if not video_id:
            raise ValueError("Could not extract YouTube video ID")
        
        # 提供された情報を優先
        if provided_username:
            info.username = provided_username
            print(f"✓ Using provided username: {provided_username}")
        
        if provided_caption:
            info.description = provided_caption
            print(f"✓ Using provided caption: {provided_caption[:100]}")
        
        # 提供されていない場合はメタデータから取得
        if not info.username or not info.description:
            metadata = _fetch_youtube_metadata(info.url, video_id)
            
            if not info.username:
                info.username = metadata.get('channel', 'YouTube')
                print(f"✓ Extracted username: {info.username}")
            
            if not info.description:
                info.description = metadata.get('title', 'YouTube動画をチェック！')
                print(f"✓ Extracted title: {info.description[:100]}")
        
        # ハッシュタグを生成
        if provided_hashtags:
            # カスタムハッシュタグが提供されている場合
            info.hashtag = format_hashtags(provided_hashtags)
            print(f"✓ Using provided hashtags: {info.hashtag}")
        else:
            # デフォルトハッシュタグ
            if info.username == 'YouTube':
                info.hashtag = '#YouTube'
            else:
                clean_username = info.username.replace(' ', '').replace('@', '')
                info.hashtag = f'#{clean_username}'
        
        print(f"✓ Final username: {info.username}")
        print(f"✓ Final description: {info.description[:100]}")
        print(f"✓ Final hashtag: {info.hashtag}")
        
        return info
        
    except Exception as e:
        print(f"Error extracting YouTube info: {e}")
        import traceback
        traceback.print_exc()
        
        # フォールバック
        info.url = _normalize_youtube_url(url)
        info.username = provided_username or 'YouTube'
        info.description = provided_caption or 'YouTube動画をチェック！'
        info.hashtag = format_hashtags(provided_hashtags) if provided_hashtags else '#YouTube'
        
        return info


def _normalize_youtube_url(url):
    """YouTube URLを正規化"""
    # youtu.be形式を展開
    if 'youtu.be/' in url:
        video_id = url.split('youtu.be/')[-1].split('?')[0].split('&')[0]
        return f'https://www.youtube.com/watch?v={video_id}'
    
    # 既に正規形式の場合
    if 'youtube.com/watch?v=' in url:
        # クエリパラメータをクリーンアップ（v=のみ残す）
        video_id = _extract_video_id(url)
        if video_id:
            return f'https://www.youtube.com/watch?v={video_id}'
    
    # Shorts形式
    if 'youtube.com/shorts/' in url:
        video_id = url.split('/shorts/')[-1].split('?')[0]
        return f'https://www.youtube.com/watch?v={video_id}'
    
    return url


def _extract_video_id(url):
    """YouTube URLから動画IDを抽出"""
    # パターン1: watch?v=
    match = re.search(r'[?&]v=([a-zA-Z0-9_-]{11})', url)
    if match:
        return match.group(1)
    
    # パターン2: youtu.be/
    match = re.search(r'youtu\.be/([a-zA-Z0-9_-]{11})', url)
    if match:
        return match.group(1)
    
    # パターン3: shorts/
    match = re.search(r'/shorts/([a-zA-Z0-9_-]{11})', url)
    if match:
        return match.group(1)
    
    return None


def _fetch_youtube_metadata(url, video_id):
    """YouTube動画のメタデータを取得"""
    metadata = {
        'title': '',
        'channel': ''
    }
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8',
        }
        
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # タイトルを取得
            og_title = soup.find('meta', property='og:title')
            if og_title and 'content' in og_title.attrs:
                metadata['title'] = og_title['content']
                print(f"✓ Extracted title from OG tag: {metadata['title'][:100]}")
            
            # チャンネル名を取得
            # 方法1: link[itemprop="name"]
            channel_link = soup.find('link', itemprop='name')
            if channel_link and 'content' in channel_link.attrs:
                metadata['channel'] = channel_link['content']
                print(f"✓ Extracted channel from itemprop: {metadata['channel']}")
            
            # 方法2: meta[name="author"]
            if not metadata['channel']:
                author_meta = soup.find('meta', attrs={'name': 'author'})
                if author_meta and 'content' in author_meta.attrs:
                    metadata['channel'] = author_meta['content']
                    print(f"✓ Extracted channel from author meta: {metadata['channel']}")
    
    except Exception as e:
        print(f"Failed to fetch YouTube metadata: {e}")
    
    return metadata
