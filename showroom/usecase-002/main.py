# showroom/usecase-002/main.py
from agents import Agent, Runner
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
from agents import set_default_openai_key

set_default_openai_key(openai_api_key)

# 予約に関する問い合わせを処理するサブエージェント
booking_agent = Agent(
    name="Booking Agent",
    instructions="航空券やホテルの予約に関する質問に答えてください。例：予約手続きの確認。",
    model="o3-mini",
)

# 返金に関する問い合わせを処理するサブエージェント
refund_agent = Agent(
    name="Refund Agent",
    instructions="購入したチケットや商品の返金に関する質問に答えてください。例：返金手続きの案内。",
    model="o3-mini",
)

# ユーザーの問い合わせを判定し、適切なサブエージェントへ委譲する triage エージェント
triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "ユーザーの質問内容に応じて、適切なエージェントへ手渡ししてください。"
        "もし質問に「予約」が含まれていれば booking_agent、"
        "「返金」が含まれていれば refund_agent へ委譲してください。"
    ),
    handoffs=[booking_agent, refund_agent],
    model="o3-mini",
)

if __name__ == "__main__":
    queries = ["航空券の予約をお願いします。", "チケットの返金手続きを教えてください。"]

    print("【Usecase-002】")
    for query in queries:
        result = Runner.run_sync(triage_agent, query)
        print("Query:", query)
        print("Response:", result.final_output)
        print("-" * 40)

    # 例として期待される出力：
    # Query: 航空券の予約をお願いします。
    # Response: (booking_agent による予約処理の回答例)
    #
    # Query: チケットの返金手続きを教えてください。
    # Response: (refund_agent による返金処理の回答例)
