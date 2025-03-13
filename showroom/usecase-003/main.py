# showroom/usecase-003/main.py
from agents import Agent, Runner
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
from agents import set_default_openai_key

set_default_openai_key(openai_api_key)

# コンテキストを使用して会話履歴を保持するエージェントの例
# Context: エージェントが会話の履歴や状態を保持するための機能


# 動的に指示を生成する関数
def get_instructions(context_wrapper, agent):
    # コンテキストから会話履歴を取得
    conversation_history = context_wrapper.context.get("conversation_history", [])

    # 基本の指示
    instructions = """
    ユーザーとの会話履歴を参照して、一貫性のある応答をしてください。
    ユーザーの過去の発言や情報（名前、趣味など）を覚えておき、質問に対して一貫性のある応答を行ってください。
    """

    # 会話履歴がある場合は、それを指示に追加
    if conversation_history:
        instructions += "\n\n会話履歴:\n"
        for entry in conversation_history:
            role = "ユーザー" if entry["role"] == "user" else "アシスタント"
            instructions += f"{role}: {entry['content']}\n"

    return instructions


if __name__ == "__main__":
    # エージェントの定義 - 動的な指示を使用
    agent = Agent(
        name="Context Agent",
        instructions=get_instructions,  # 関数を渡す
        model="o3-mini",
    )

    # コンテキストの作成 - 会話履歴を保持するための辞書
    context = {"conversation_history": []}  # 会話履歴を保存するリスト

    print("【Usecase-003: Context の活用】")
    print("コンテキストを使用して会話の履歴を保持する例")
    print("-" * 40)

    # 最初の質問
    query1 = "私の名前は田中です。"
    result1 = Runner.run_sync(agent, query1, context=context)
    # 会話履歴をコンテキストに追加
    context["conversation_history"].append({"role": "user", "content": query1})
    context["conversation_history"].append(
        {"role": "assistant", "content": result1.final_output}
    )
    print("Query 1:", query1)
    print("Response 1:", result1.final_output)
    print("-" * 40)

    # 2回目の質問 - コンテキストが保持されているため、名前を覚えている
    query2 = "私の名前は何ですか？"
    result2 = Runner.run_sync(agent, query2, context=context)
    # 会話履歴をコンテキストに追加
    context["conversation_history"].append({"role": "user", "content": query2})
    context["conversation_history"].append(
        {"role": "assistant", "content": result2.final_output}
    )
    print("Query 2:", query2)
    print("Response 2:", result2.final_output)
    print("-" * 40)

    # 3回目の質問 - さらに情報を追加
    query3 = "私の趣味は読書です。"
    result3 = Runner.run_sync(agent, query3, context=context)
    # 会話履歴をコンテキストに追加
    context["conversation_history"].append({"role": "user", "content": query3})
    context["conversation_history"].append(
        {"role": "assistant", "content": result3.final_output}
    )
    print("Query 3:", query3)
    print("Response 3:", result3.final_output)
    print("-" * 40)

    # 4回目の質問 - 名前と趣味の両方を覚えている
    query4 = "私の名前と趣味を教えてください。"
    result4 = Runner.run_sync(agent, query4, context=context)
    print("Query 4:", query4)
    print("Response 4:", result4.final_output)

    # 例として期待される出力：
    # Query 1: 私の名前は田中です。
    # Response 1: こんにちは、田中さん。お手伝いできることがあれば教えてください。
    #
    # Query 2: 私の名前は何ですか？
    # Response 2: あなたの名前は田中さんです。
    #
    # Query 3: 私の趣味は読書です。
    # Response 3: 読書が趣味なんですね。素晴らしい趣味をお持ちです。
    #
    # Query 4: 私の名前と趣味を教えてください。
    # Response 4: あなたは田中さんで、趣味は読書です。
