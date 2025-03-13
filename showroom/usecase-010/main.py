# showroom/usecase-010/main.py
from agents import Agent, Runner
from dotenv import load_dotenv
import os
import time
import sys

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
from agents import set_default_openai_key

set_default_openai_key(openai_api_key)

# Streaming: エージェントからの応答をリアルタイムでトークンごとに受け取る機能
# ユーザーエクスペリエンスを向上させるために、応答が生成されるたびに表示できます

if __name__ == "__main__":
    # 基本的なエージェントの定義
    agent = Agent(
        name="Streaming Agent",
        instructions="ユーザーの質問に詳細かつ段階的に回答してください。",
        model="o3-mini",
    )

    print("【Usecase-010: Streaming の活用】")
    print("エージェントからの応答をリアルタイムで受け取る例")
    print("-" * 40)

    # ストリーミングを使用しない通常の実行
    query = (
        "人工知能の歴史について、5つの重要なマイルストーンを挙げて説明してください。"
    )
    print("Query:", query)

    print("\n通常の実行（ストリーミングなし）:")
    start_time = time.time()
    result = Runner.run_sync(agent, query)
    end_time = time.time()

    print(result.final_output)
    print(f"\n実行時間: {end_time - start_time:.2f}秒")
    print("-" * 40)

    # ストリーミングを使用した実行
    print("\nストリーミング実行:")
    print("（トークンごとにリアルタイムで表示されます）")

    import asyncio

    # 非同期処理を実行する関数
    async def run_streaming():
        start_time = time.time()

        # ストリーミングモードでエージェントを実行
        result = Runner.run_streamed(agent, query)

        # ストリーミングイベントを処理
        async for event in result.stream_events():
            # イベントの構造をデバッグ出力
            # print(f"Event type: {type(event)}", file=sys.stderr)
            # print(f"Event: {event}", file=sys.stderr)

            if hasattr(event, "data"):
                # print(f"Event.data type: {type(event.data)}", file=sys.stderr)
                # print(f"Event.data: {event.data}", file=sys.stderr)

                if hasattr(event.data, "delta"):
                    delta = event.data.delta
                    # print(f"Delta type: {type(delta)}", file=sys.stderr)
                    # print(f"Delta: {delta}", file=sys.stderr)

                    # deltaが文字列の場合
                    if isinstance(delta, str) and delta:
                        print(delta, end="", flush=True)
                    # deltaがオブジェクトでcontentプロパティを持つ場合
                    elif hasattr(delta, "content") and delta.content:
                        print(delta.content, end="", flush=True)

        end_time = time.time()
        print(f"\n\n実行時間: {end_time - start_time:.2f}秒")

    # 非同期関数を実行
    asyncio.run(run_streaming())

    # 例として期待される出力：
    # 通常の実行（ストリーミングなし）:
    # （完全な応答が一度に表示される）
    # 人工知能の歴史における5つの重要なマイルストーン：
    #
    # 1. チューリングテストの提案（1950年）...
    #
    # ストリーミング実行:
    # （トークンごとにリアルタイムで表示されます）
    # 人工知能の歴史における5つの重要なマイルストーン：
    #
    # 1. チューリング...（トークンごとに徐々に表示される）
