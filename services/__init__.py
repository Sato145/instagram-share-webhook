"""
Social Media Share Services
各SNSプラットフォームの情報抽出サービス
"""

class SocialMediaInfo:
    """SNS投稿情報の統一データモデル"""
    
    def __init__(self):
        self.platform = ''        # 'instagram', 'tiktok', etc.
        self.username = ''        # ユーザー名
        self.description = ''     # 投稿本文
        self.url = ''            # 投稿URL
        self.post_code = ''      # 投稿ID/コード
        self.type = ''           # 投稿タイプ（投稿/リール/動画）
        self.is_video = False    # 動画かどうか
        self.hashtag = ''        # ハッシュタグ
        self.emoji = ''          # 絵文字
    
    def to_dict(self):
        """辞書形式に変換"""
        return {
            'platform': self.platform,
            'username': self.username,
            'description': self.description,
            'url': self.url,
            'post_code': self.post_code,
            'type': self.type,
            'is_video': self.is_video,
            'hashtag': self.hashtag,
            'emoji': self.emoji
        }
