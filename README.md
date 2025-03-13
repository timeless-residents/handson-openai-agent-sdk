# OpenAI Agent SDK ハンズオン

このリポジトリは、OpenAI Agent SDKを使用した実践的なサンプルコードを提供します。Agent SDKを使って、高度なAIエージェントを簡単に構築・カスタマイズする方法を学ぶことができます。

## 概要

OpenAI Agent SDKは、大規模言語モデル（LLM）を活用したインテリジェントなエージェントを構築するためのフレームワークです。このSDKを使用することで、以下のような機能を持つエージェントを簡単に作成できます：

- 自然言語による指示に基づいた応答生成
- カスタム関数ツールの実行
- 複数エージェント間の連携（ハンドオフ）
- コンテキスト管理
- 構造化データの出力
- 動的な指示変更
- ライフサイクルイベントの監視
- ガードレールによる安全性確保
- リアルタイムストリーミング応答

## 前提条件

- Python 3.8以上
- OpenAI APIキー

## インストール

```bash
pip install agents
```

## 環境設定

1. `.env`ファイルを作成し、OpenAI APIキーを設定します：

```
OPENAI_API_KEY=your_api_key_here
```

2. 以下のコードでAPIキーを読み込みます：

```python
from dotenv import load_dotenv
import os
from agents import set_default_openai_key

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)
```

## ユースケース

このリポジトリには、Agent SDKの様々な機能を紹介する11のユースケースが含まれています。

### Usecase-000: 基本的な使用方法

最もシンプルなエージェントの作成と実行方法を示します。

```python
from agents import Agent, Runner

agent = Agent(
    name="Assistant", 
    instructions="You are a helpful assistant", 
    model="gpt-4o"
)

result = Runner.run_sync(
    agent,
    "Write the haiku about recursion in programming. Japanese language.",
)
print(result.final_output)
```

### Usecase-001: Function Tools

カスタム関数をエージェントのツールとして定義し、エージェントがそれらを呼び出せるようにします。

```python
from agents import Agent, function_tool, Runner

@function_tool
def get_weather(city: str) -> str:
    return f"{city} の天気は晴れです"

agent = Agent(
    name="Haiku Agent",
    instructions="常に俳句形式で回答してください。",
    model="o3-mini",
    tools=[get_weather],
)

result = Runner.run_sync(agent, "東京の天気を教えてください")
print(result.final_output)
```

### Usecase-002: Agent Handoffs

複数のエージェントを連携させ、特定の条件に基づいて別のエージェントに処理を委譲する方法を示します。

```python
booking_agent = Agent(
    name="Booking Agent",
    instructions="航空券やホテルの予約に関する質問に答えてください。",
    model="o3-mini",
)

refund_agent = Agent(
    name="Refund Agent",
    instructions="返金に関する質問に答えてください。",
    model="o3-mini",
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="質問内容に応じて、適切なエージェントへ手渡ししてください。",
    handoffs=[booking_agent, refund_agent],
    model="o3-mini",
)
```

### Usecase-003: Context

エージェントが会話の履歴や状態を保持するためのコンテキスト機能を活用する方法を示します。

```python
def get_instructions(context_wrapper, agent):
    conversation_history = context_wrapper.context.get("conversation_history", [])
    instructions = "ユーザーとの会話履歴を参照して、一貫性のある応答をしてください。"
    
    if conversation_history:
        instructions += "\n\n会話履歴:\n"
        for entry in conversation_history:
            role = "ユーザー" if entry["role"] == "user" else "アシスタント"
            instructions += f"{role}: {entry['content']}\n"
    
    return instructions

agent = Agent(
    name="Context Agent",
    instructions=get_instructions,
    model="o3-mini",
)

context = {"conversation_history": []}
```

### Usecase-004: Output Types

Pydanticモデルを使用して、エージェントからの応答を構造化データとして受け取る方法を示します。

```python
from pydantic import BaseModel, Field
from typing import List, Dict

class ProductReview(BaseModel):
    product_name: str = Field(description="レビュー対象の商品名")
    rating: int = Field(description="評価（1-5の整数）", ge=1, le=5)
    pros: List[str] = Field(description="商品の良い点のリスト")
    cons: List[str] = Field(description="商品の改善点のリスト")
    summary: str = Field(description="レビューの要約")
    recommendation: bool = Field(description="他の人にお勧めするかどうか")

review_agent = Agent(
    name="Review Agent",
    instructions="商品レビューリクエストに対して、詳細な構造化レビューを提供してください。",
    model="o3-mini",
)
```

### Usecase-005: Dynamic Instructions

エージェントの指示を実行時に動的に変更する方法を示します。

```python
agent = Agent(
    name="Dynamic Agent",
    instructions="標準的な応答をしてください。",
    model="o3-mini",
)

# 基本の指示での応答
result1 = Runner.run_sync(agent, "東京の観光スポットを教えてください。")

# 指示を変更: 箇条書きで回答するように
agent.instructions = "必ず箇条書き（・で始まる行）で回答してください。"
result2 = Runner.run_sync(agent, "東京の観光スポットを教えてください。")
```

### Usecase-006: Lifecycle Events

エージェント実行中のイベントをモニタリングして対応するための機能を示します。

```python
from agents import lifecycle

class CustomRunHooks(lifecycle.RunHooks):
    async def on_agent_start(self, context, agent):
        import time
        context.start_time = time.time()
        print(f"[イベント] エージェント実行開始: {agent.name}")

    async def on_agent_end(self, context, agent, output):
        import time
        end_time = time.time()
        elapsed_time = end_time - context.start_time
        print(f"[イベント] エージェント実行終了: {agent.name}")
        print(f"[イベント] 実行時間: {elapsed_time:.2f}秒")

result = Runner.run_sync(agent, query, hooks=CustomRunHooks())
```

### Usecase-007: Guardrails

エージェントの応答に対する安全メカニズムを提供する機能を示します。

```python
guardrails_agent = Agent(
    name="Guardrails Agent",
    instructions="""
    ユーザーの質問に詳細に回答してください。
    
    ただし、以下のルールを厳守してください：
    1. 政治的な内容には「政治的な話題についてはお答えできません」と回答する
    2. 違法行為に関する質問には「違法行為についての情報は提供できません」と回答する
    3. 医療アドバイスを求められた場合は「医療的なアドバイスは医師に相談してください」と回答する
    4. 個人情報の要求には応じない
    5. 常に丁寧な言葉遣いを維持する
    """,
    model="o3-mini",
)
```

### Usecase-008: Agent Clone

既存のエージェントのコピーを作成し、プロパティを変更する機能を示します。

```python
base_translator = Agent(
    name="Base Translator",
    instructions="入力されたテキストを指定された言語に翻訳してください。",
    model="o3-mini",
)

french_translator = base_translator.clone(
    name="French Translator",
    instructions="入力されたテキストをフランス語に翻訳してください。フランス語の自然な表現を心がけてください。",
)
```

### Usecase-009: 複数機能の組み合わせ

Function Tools、Dynamic Instructions、Contextなどの機能を組み合わせた高度なエージェントの例を示します。

```python
@function_tool
def get_all_tasks() -> List[Dict]:
    """すべてのタスクを取得します。"""
    return memory_store["tasks"]

task_agent = Agent(
    name="Task Manager",
    instructions="""
    あなたはタスク管理アシスタントです。
    ユーザーのタスク管理を手伝います。
    """,
    model="o3-mini",
    tools=[get_all_tasks, get_task, add_task, complete_task],
)

# 特定の対話でエージェントの指示を動的に変更
task_agent.instructions = """
あなたはタスク管理アシスタントです。
タスク一覧を表示する際は、特に指定がない限り未完了のタスクのみを表示してください。
"""
```

### Usecase-010: Streaming

エージェントからの応答をリアルタイムでトークンごとに受け取る機能を示します。

```python
import asyncio

async def run_streaming():
    start_time = time.time()
    
    # ストリーミングモードでエージェントを実行
    result = Runner.run_streamed(agent, query)
    
    # ストリーミングイベントを処理
    async for event in result.stream_events():
        if (
            hasattr(event, "data")
            and hasattr(event.data, "delta")
            and event.data.delta
        ):
            # deltaが文字列の場合
            if isinstance(event.data.delta, str) and event.data.delta:
                print(event.data.delta, end="", flush=True)
            # deltaがオブジェクトでcontentプロパティを持つ場合
            elif hasattr(event.data.delta, "content") and event.data.delta.content:
                print(event.data.delta.content, end="", flush=True)
    
    end_time = time.time()
    print(f"\n\n実行時間: {end_time - start_time:.2f}秒")

# 非同期関数を実行
asyncio.run(run_streaming())
```

## 主な機能

### Agent

`Agent`クラスは、AIエージェントの基本的な構成要素です。以下のパラメータで初期化できます：

- `name`: エージェントの名前
- `instructions`: エージェントの振る舞いを定義する指示
- `model`: 使用するモデル（例：`"gpt-4o"`、`"o3-mini"`）
- `tools`: エージェントが使用できるツールのリスト
- `handoffs`: エージェントが処理を委譲できる他のエージェントのリスト

### Runner

`Runner`クラスは、エージェントの実行を管理します。主なメソッドは以下の通りです：

- `run_sync`: エージェントを同期的に実行します
- `run`: エージェントを非同期的に実行します
- `run_streamed`: エージェントをストリーミングモードで実行します

### Function Tool

`function_tool`デコレータを使用して、Pythonの関数をエージェントが使用できるツールとして定義できます。

```python
@function_tool
def get_weather(city: str) -> str:
    # 天気情報を取得するロジック
    return f"{city} の天気は晴れです"
```

### Context

コンテキストは、エージェントが会話の履歴や状態を保持するために使用されます。`Runner.run_sync`メソッドの`context`パラメータに辞書を渡すことで、エージェント間で情報を共有できます。

### Output Types

Pydanticモデルを使用して、エージェントからの応答を構造化データとして定義できます。これにより、応答を簡単に解析して処理できます。

## 応用例

Agent SDKを使用した応用例：

1. **カスタマーサポートボット**: 質問の種類に応じて適切な部門のエージェントに転送
2. **データ分析アシスタント**: データベースからの情報取得と分析を行うツールを持つエージェント
3. **コンテンツ生成ツール**: 特定のフォーマットや制約に従ってコンテンツを生成するエージェント
4. **タスク管理アシスタント**: タスクの追加、更新、完了を管理するエージェント
5. **多言語翻訳サービス**: 様々な言語間で翻訳を行うエージェント

## 参考リソース

- [OpenAI Agent SDK 公式ドキュメント](https://github.com/openai/agents)
- [OpenAI API リファレンス](https://platform.openai.com/docs/api-reference)

## ライセンス

このプロジェクトは[MITライセンス](LICENSE)の下で公開されています。
