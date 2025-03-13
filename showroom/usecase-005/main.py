# showroom/usecase-005/main.py
from agents import Agent, Runner
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
from agents import set_default_openai_key

set_default_openai_key(openai_api_key)

# Dynamic Instructions: 実行時に指示を動的に変更する機能
# エージェントの振る舞いを実行時に変更できます

if __name__ == "__main__":
    # 基本的なエージェントの定義
    agent = Agent(
        name="Dynamic Agent",
        instructions="標準的な応答をしてください。",
        model="o3-mini",
    )

    print("【Usecase-005: Dynamic Instructions の活用】")
    print("エージェントの指示を実行時に動的に変更する例")
    print("-" * 40)

    # 基本の指示での応答
    query1 = "東京の観光スポットを教えてください。"
    result1 = Runner.run_sync(agent, query1)
    print("Query 1:", query1)
    print("基本指示での応答:")
    print(result1.final_output)
    print("-" * 40)

    # 指示を変更: 箇条書きで回答するように
    agent.instructions = "必ず箇条書き（・で始まる行）で回答してください。"
    query2 = "東京の観光スポットを教えてください。"
    result2 = Runner.run_sync(agent, query2)
    print("Query 2:", query2)
    print("箇条書き指示での応答:")
    print(result2.final_output)
    print("-" * 40)

    # 指示を変更: 英語で回答するように
    agent.instructions = "必ず英語で回答してください。"
    query3 = "東京の観光スポットを教えてください。"
    result3 = Runner.run_sync(agent, query3)
    print("Query 3:", query3)
    print("英語指示での応答:")
    print(result3.final_output)
    print("-" * 40)

    # 指示を変更: 俳句形式で回答するように
    agent.instructions = "必ず俳句形式（5-7-5の17音）で回答してください。"
    query4 = "東京の観光スポットを教えてください。"
    result4 = Runner.run_sync(agent, query4)
    print("Query 4:", query4)
    print("俳句指示での応答:")
    print(result4.final_output)

    # 例として期待される出力：
    # 基本指示での応答:
    # 東京には多くの観光スポットがあります。代表的なものとして、東京スカイツリー、浅草寺、東京タワー、渋谷スクランブル交差点、新宿御苑、上野公園、お台場、築地市場（現在は豊洲市場）などがあります。
    #
    # 箇条書き指示での応答:
    # ・東京スカイツリー
    # ・浅草寺
    # ・東京タワー
    # ・渋谷スクランブル交差点
    # ・新宿御苑
    # ・上野公園
    # ・お台場
    # ・豊洲市場
    #
    # 英語指示での応答:
    # Tokyo has many famous tourist attractions. Some of the most popular ones include Tokyo Skytree, Sensoji Temple, Tokyo Tower, Shibuya Crossing, Shinjuku Gyoen National Garden, Ueno Park, Odaiba, and Toyosu Market.
    #
    # 俳句指示での応答:
    # 空高く立つ
    # スカイツリー浅草
    # 人の波
