"""
投稿テンプレート生成モジュール
"""

from services.common import shorten_text


def create_tweet_text(info):
    """SNS投稿情報からX投稿文を生成"""
    
    # 本文を短縮（100文字まで）
    description = shorten_text(info.description, 100)
    
    # プラットフォーム別の表示名
    display_name = _get_display_name(info)
    
    # テンプレート適用
    if description and description not in ['Instagram投稿をチェック！', 'TikTok動画をチェック！']:
        tweet_text = f"{info.emoji} {display_name}さんの{info.type}\n\n{description}\n\n{info.url}\n\n{info.hashtag}"
    else:
        tweet_text = f"{info.emoji} {display_name}さんの{info.type}\n\n{info.url}\n\n{info.hashtag}"
    
    return tweet_text


def create_pushover_message(info):
    """SNS投稿情報からPushover通知メッセージを生成"""
    
    # プラットフォーム別の表示名
    display_name = _get_display_name(info)
    
    # 通知メッセージを構築
    message_parts = [
        f"{info.emoji} {display_name}さんの{info.type}"
    ]
    
    # 本文がある場合は追加（最大200文字）
    if info.description:
        desc = shorten_text(info.description, 200)
        message_parts.append(f"\n📝 {desc}")
    
    # URLを追加
    message_parts.append(f"\n\n🔗 {info.url}")
    
    # ハッシュタグを追加
    message_parts.append(f"\n\n{info.hashtag}")
    
    message_parts.append("\n\n👇 タップしてXに投稿")
    
    return ''.join(message_parts)


def create_pushover_title(info):
    """Pushover通知のタイトルを生成"""
    platform_name = info.platform.title()
    return f'{info.emoji} {platform_name} {info.type}を共有'


def _get_display_name(info):
    """プラットフォームに応じた表示名を取得"""
    if info.platform == 'tiktok':
        # TikTokの場合は@付き
        return f'@{info.username}'
    else:
        # Instagramなどは@なし
        return info.username
