"""
共通処理モジュール
プラットフォーム検出、URL処理など
"""

import re
from urllib.parse import quote


def detect_platform(url):
    """URLからプラットフォームを検出"""
    url_lower = url.lower()
    
    if 'instagram.com' in url_lower:
        return 'instagram'
    elif 'tiktok.com' in url_lower or 'vt.tiktok.com' in url_lower:
        return 'tiktok'
    elif 'youtube.com' in url_lower or 'youtu.be' in url_lower:
        return 'youtube'
    else:
        return None


def clean_url(url):
    """URLをクリーンアップ（クエリパラメータ削除など）"""
    # クエリパラメータを削除
    clean = url.split('?')[0].rstrip('/')
    return clean


def create_hashtag(username, platform):
    """ユーザー名とプラットフォームからハッシュタグを生成"""
    if not username or username in ['Instagram', 'TikTok', 'YouTube']:
        return f'#{platform.title()}'
    
    # ユーザー名をハッシュタグ化（スペースや特殊文字を削除）
    clean_username = username.replace(' ', '').replace('@', '')
    return f'#{clean_username}'


def create_twitter_intent_url(tweet_text):
    """X投稿用のIntent URLを生成"""
    encoded_text = quote(tweet_text)
    return f"https://twitter.com/intent/tweet?text={encoded_text}"


def shorten_text(text, max_length=100):
    """テキストを指定文字数に短縮"""
    if not text:
        return ''
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length] + '...'
