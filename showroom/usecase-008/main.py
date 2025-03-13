# showroom/usecase-008/main.py
from agents import Agent, Runner
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
from agents import set_default_openai_key

set_default_openai_key(openai_api_key)

# Agent Clone: 既存のエージェントのコピーを作成し、プロパティを変更する機能
# 基本設定を維持しながら、特定の属性だけを変更したバリエーションを作成できます

if __name__ == "__main__":
    # 基本となる翻訳エージェントの定義
    base_translator = Agent(
        name="Base Translator",
        instructions="入力されたテキストを指定された言語に翻訳してください。",
        model="o3-mini",
    )

    print("【Usecase-008: Agent Clone の活用】")
    print("既存のエージェントをクローンして属性を変更する例")
    print("-" * 40)

    # 基本エージェントの実行
    query_ja = "こんにちは、世界。今日はいい天気ですね。"
    print("元のテキスト:", query_ja)
    print("\n基本翻訳エージェント（デフォルト設定）:")
    result_base = Runner.run_sync(
        base_translator, f"次のテキストを英語に翻訳してください: '{query_ja}'"
    )
    print(result_base.final_output)
    print("-" * 40)

    # クローン1: フランス語翻訳に特化
    french_translator = base_translator.clone(
        name="French Translator",
        instructions="入力されたテキストをフランス語に翻訳してください。フランス語の自然な表現を心がけてください。",
    )

    print("\nフランス語翻訳エージェント（クローン1）:")
    result_french = Runner.run_sync(
        french_translator, f"次のテキストを翻訳してください: '{query_ja}'"
    )
    print(result_french.final_output)
    print("-" * 40)

    # クローン2: ビジネス文書翻訳に特化
    business_translator = base_translator.clone(
        name="Business Translator",
        instructions="入力されたテキストを英語に翻訳してください。ビジネス文書に適した丁寧で専門的な表現を使用してください。",
    )

    print("\nビジネス翻訳エージェント（クローン2）:")
    result_business = Runner.run_sync(
        business_translator, f"次のテキストを翻訳してください: '{query_ja}'"
    )
    print(result_business.final_output)
    print("-" * 40)

    # クローン3: カジュアルな表現に特化
    casual_translator = base_translator.clone(
        name="Casual Translator",
        instructions="入力されたテキストを英語に翻訳してください。若者向けのカジュアルな表現やスラングを使用してください。",
    )

    print("\nカジュアル翻訳エージェント（クローン3）:")
    result_casual = Runner.run_sync(
        casual_translator, f"次のテキストを翻訳してください: '{query_ja}'"
    )
    print(result_casual.final_output)

    # 例として期待される出力：
    # 基本翻訳エージェント（デフォルト設定）:
    # Hello, world. It's nice weather today.
    #
    # フランス語翻訳エージェント（クローン1）:
    # Bonjour, le monde. Il fait beau aujourd'hui.
    #
    # ビジネス翻訳エージェント（クローン2）:
    # Good day. The weather conditions are favorable today.
    #
    # カジュアル翻訳エージェント（クローン3）:
    # Hey there! Awesome weather we're having today, right?
