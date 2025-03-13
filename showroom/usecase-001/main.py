# showroom/usecase-001/main.py
from agents import Agent, function_tool, Runner, set_default_openai_key
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)


# ツールとして天気情報取得関数を定義
@function_tool
def get_weather(city: str) -> str:
    # 実際にはAPI連携などで天気を取得しますが、ここではシンプルに固定の結果を返します
    return f"{city} の天気は晴れです"


# エージェントを定義（常に俳句形式で回答する）
agent = Agent(
    name="Haiku Agent",
    instructions="常に俳句形式で回答してください。例えば、1行目で季節感、2行目で都市名、3行目で結論を表現する。",
    model="o3-mini",
    tools=[get_weather],
)

if __name__ == "__main__":
    print("Starting Haiku Agent...")
    # クエリ例: 東京の天気について問い合わせ
    query = "東京の天気を教えてください"
    print("Sending query to agent...")
    result = Runner.run_sync(agent, query)
    print("Got result from agent")

    print("【Usecase-001】")
    print("Query:", query)
    print("Response:", result.final_output)
    # 例として期待される出力（エージェントの指示に沿って俳句形式の回答となる）
    # 例:
    # 「朝露に
    # 東京の空
    # 晴れ渡る」
