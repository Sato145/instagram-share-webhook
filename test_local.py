#!/usr/bin/env python3
"""
ローカルテスト用スクリプト
Renderにデプロイする前にローカルで動作確認
"""

import requests
import json
import os
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

def test_webhook(url, instagram_url):
    """Webhookエンドポイントをテスト"""
    
    print(f"\n{'='*60}")
    print(f"Webhook テスト")
    print(f"{'='*60}\n")
    
    print(f"サーバーURL: {url}")
    print(f"Instagram URL: {instagram_url}\n")
    
    try:
        # POSTリクエスト送信
        response = requests.post(
            f"{url}/webhook",
            json={"url": instagram_url},
            timeout=30
        )
        
        print(f"ステータスコード: {response.status_code}")
        print(f"\nレスポンス:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
        if response.status_code == 200:
            print(f"\n✅ テスト成功！")
            print(f"Pushover通知を確認してください")
        else:
            print(f"\n❌ テスト失敗")
        
        return response.status_code == 200
        
    except requests.exceptions.ConnectionError:
        print(f"\n❌ 接続エラー")
        print(f"サーバーが起動しているか確認してください:")
        print(f"  python app.py")
        return False
        
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        return False

def test_health(url):
    """ヘルスチェックエンドポイントをテスト"""
    
    print(f"\n{'='*60}")
    print(f"ヘルスチェック")
    print(f"{'='*60}\n")
    
    try:
        response = requests.get(f"{url}/health", timeout=10)
        
        print(f"ステータスコード: {response.status_code}")
        print(f"\nレスポンス:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
        if response.status_code == 200:
            print(f"\n✅ サーバーは正常に動作しています")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        return False

def main():
    """メイン処理"""
    
    print("\n" + "="*60)
    print("Instagram Share Webhook - ローカルテスト")
    print("="*60)
    
    # テスト対象URL
    local_url = "http://localhost:5000"
    
    # テスト用Instagram URL
    test_urls = [
        "https://www.instagram.com/p/C3xXxXxXxXx/",  # 通常投稿
        "https://www.instagram.com/reel/C3xXxXxXxXx/",  # リール
    ]
    
    # 環境変数チェック
    pushover_token = os.environ.get('PUSHOVER_TOKEN')
    pushover_user = os.environ.get('PUSHOVER_USER')
    
    if not pushover_token or not pushover_user:
        print("\n⚠️  警告: Pushover環境変数が設定されていません")
        print("通知は送信されませんが、他の機能はテストできます\n")
        print("環境変数を設定するには:")
        print("  1. .env.example を .env にコピー")
        print("  2. .env にPushover認証情報を入力")
        print("  3. このスクリプトを再実行\n")
    
    # ヘルスチェック
    if not test_health(local_url):
        print("\n❌ サーバーが起動していません")
        print("\n起動方法:")
        print("  python app.py")
        return 1
    
    # Webhookテスト
    success_count = 0
    for i, instagram_url in enumerate(test_urls, 1):
        print(f"\n{'='*60}")
        print(f"テスト {i}/{len(test_urls)}")
        print(f"{'='*60}")
        
        if test_webhook(local_url, instagram_url):
            success_count += 1
    
    # 結果サマリー
    print(f"\n{'='*60}")
    print(f"テスト結果")
    print(f"{'='*60}\n")
    print(f"成功: {success_count}/{len(test_urls)}")
    
    if success_count == len(test_urls):
        print(f"\n✅ すべてのテストが成功しました！")
        print(f"\n次のステップ:")
        print(f"  1. GitHubにプッシュ")
        print(f"  2. Renderにデプロイ")
        print(f"  3. iPhoneショートカットを設定")
    else:
        print(f"\n⚠️  一部のテストが失敗しました")
        print(f"ログを確認して問題を修正してください")
    
    print("\n")
    
    return 0 if success_count == len(test_urls) else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
