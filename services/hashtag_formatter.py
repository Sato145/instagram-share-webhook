"""
ハッシュタグフォーマッター
"""


def format_hashtags(hashtags_input):
    """
    ハッシュタグ文字列をフォーマット
    
    入力例:
    - "STU48 アイドル 瀬戸内"
    - "#STU48 #アイドル"（既に#がある場合も対応）
    - "STU48"
    
    出力例:
    - "#STU48 #アイドル #瀬戸内"
    """
    if not hashtags_input or not hashtags_input.strip():
        return ''
    
    # 入力をトリム
    hashtags_input = hashtags_input.strip()
    
    # スペースで分割
    tags = hashtags_input.split()
    
    # 各タグに#を付与（既に#がある場合は付与しない）
    formatted_tags = []
    for tag in tags:
        tag = tag.strip()
        if not tag:
            continue
        
        # 既に#で始まっている場合はそのまま
        if tag.startswith('#'):
            formatted_tags.append(tag)
        else:
            # #を付与
            formatted_tags.append(f'#{tag}')
    
    # スペース区切りで結合
    return ' '.join(formatted_tags)
