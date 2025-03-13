# showroom/usecase-006/main.py
from agents import Agent, Runner, lifecycle
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
from agents import set_default_openai_key

set_default_openai_key(openai_api_key)

# Lifecycle Events: エージェント実行中のイベントをモニタリングして対応するための機能
# エージェントの実行プロセスの各段階で発生するイベントをキャプチャし、処理できます


# RunHooksを継承したカスタムフックを定義
class CustomRunHooks(lifecycle.RunHooks):
    async def on_agent_start(self, context, agent):
        # 開始時間を記録
        import time

        context.start_time = time.time()
        print(f"[イベント] エージェント実行開始: {agent.name}")

    async def on_agent_end(self, context, agent, output):
        # 実行時間を計算
        import time

        end_time = time.time()
        elapsed_time = end_time - context.start_time
        print(f"[イベント] エージェント実行終了: {agent.name}")
        print(f"[イベント] 実行時間: {elapsed_time:.2f}秒")

    async def on_tool_start(self, context, agent, tool):
        print(f"[イベント] ツール実行開始: {tool.name}")

    async def on_tool_end(self, context, agent, tool, result):
        print(f"[イベント] ツール実行終了: {tool.name}")
        print(f"[イベント] ツール結果: {result}")


if __name__ == "__main__":
    # 基本的なエージェントの定義
    agent = Agent(
        name="Lifecycle Events Agent",
        instructions="ユーザーの質問に詳細に回答してください。",
        model="o3-mini",
    )

    print("【Usecase-006: Lifecycle Events の活用】")
    print("エージェント実行中のイベントをモニタリングする例")
    print("-" * 40)

    # エージェントの実行
    query = "人工知能の歴史について簡単に説明してください。"
    print("Query:", query)

    # カスタムフックを使用してエージェントを実行
    result = Runner.run_sync(agent, query, hooks=CustomRunHooks())

    # ライフサイクルイベントの登録方法については、
    # RunHooksクラスを継承して必要なメソッドをオーバーライドします。
    # 詳細は公式ドキュメントを参照してください。

    print("\n最終応答:")
    print(result.final_output)

    # 例として期待される出力：
    # [イベント] エージェント実行開始: Lifecycle Events Agent
    # [イベント] エージェント実行終了: Lifecycle Events Agent
    # [イベント] 実行時間: 2.34秒
    #
    # 最終応答:
    # 人工知能（AI）の歴史は1950年代に始まります。コンピュータ科学者のアラン・チューリングが「機械は考えることができるか」という問いを立て、「チューリングテスト」を提案しました。
    #
    # 1956年のダートマス会議で「人工知能」という言葉が初めて使用され、この分野が正式に誕生しました。1960年代から70年代は「AIの黄金期」と呼ばれ、基本的なアルゴリズムや問題解決手法が開発されました。
    #
    # しかし、1970年代後半から1980年代は「AIの冬」と呼ばれる停滞期に入りました。期待された成果が出ず、研究資金が減少しました。
    #
    # 1990年代以降、機械学習の発展とともにAIは再び注目を集め始めました。特に2010年代以降はディープラーニングの進歩により、画像認識、自然言語処理、ゲームなどの分野で人間を超える性能を示すようになりました。
    #
    # 現在のAIは、自動運転車、医療診断、言語翻訳、推薦システムなど、様々な分野で実用化されています。
