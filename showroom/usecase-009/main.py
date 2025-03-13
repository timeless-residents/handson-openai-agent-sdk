# showroom/usecase-009/main.py
from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
from typing import List, Dict
import os
import json

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
from agents import set_default_openai_key

set_default_openai_key(openai_api_key)

# 複数の機能を組み合わせた高度なエージェントの例
# Function Tools + Dynamic Instructions + Context の組み合わせ

# データベースの代わりとなる簡易的なメモリストア
memory_store = {
    "tasks": [
        {"id": 1, "title": "買い物リスト作成", "completed": True},
        {"id": 2, "title": "レポート提出", "completed": False},
        {"id": 3, "title": "会議の準備", "completed": False},
    ]
}


# タスク管理用のツール
@function_tool
def get_all_tasks() -> List[Dict]:
    """
    すべてのタスクを取得します。
    """
    return memory_store["tasks"]


@function_tool
def get_task(task_id: int) -> Dict:
    """
    指定されたIDのタスクを取得します。

    Args:
        task_id: 取得するタスクのID
    """
    for task in memory_store["tasks"]:
        if task["id"] == task_id:
            return task
    return {"error": "タスクが見つかりません"}


@function_tool
def add_task(title: str) -> Dict:
    """
    新しいタスクを追加します。

    Args:
        title: 新しいタスクのタイトル
    """
    new_id = max([task["id"] for task in memory_store["tasks"]]) + 1
    new_task = {"id": new_id, "title": title, "completed": False}
    memory_store["tasks"].append(new_task)
    return new_task


@function_tool
def complete_task(task_id: int) -> Dict:
    """
    タスクを完了状態に変更します。

    Args:
        task_id: 完了するタスクのID
    """
    for task in memory_store["tasks"]:
        if task["id"] == task_id:
            task["completed"] = True
            return task
    return {"error": "タスクが見つかりません"}


if __name__ == "__main__":
    # タスク管理エージェントの定義
    task_agent = Agent(
        name="Task Manager",
        instructions="""
        あなたはタスク管理アシスタントです。
        ユーザーのタスク管理を手伝います。
        タスクの一覧表示、追加、完了などの操作をサポートします。
        """,
        model="o3-mini",
        tools=[get_all_tasks, get_task, add_task, complete_task],
    )

    print("【Usecase-009: 複数機能の組み合わせ】")
    print("Function Tools + Dynamic Instructions + Context の組み合わせ例")
    print("-" * 40)

    # コンテキストの作成 - 会話履歴を保持するための辞書
    context = {}

    # 会話の流れを示す例
    conversations = [
        "タスク一覧を表示してください。",
        "新しいタスク「プレゼン資料作成」を追加してください。",
        "タスク一覧を表示してください。",
        "タスクID 2を完了にしてください。",
        "未完了のタスクだけを表示してください。",
    ]

    # 会話の実行
    for i, query in enumerate(conversations, 1):
        print(f"\n対話 {i}:")
        print(f"ユーザー: {query}")

        # 特定の対話でエージェントの指示を動的に変更
        if i == 5:
            # 5回目の対話では、未完了タスクのみを表示するように指示を変更
            task_agent.instructions = """
            あなたはタスク管理アシスタントです。
            ユーザーのタスク管理を手伝います。
            タスクの一覧表示、追加、完了などの操作をサポートします。
            タスク一覧を表示する際は、特に指定がない限り未完了のタスクのみを表示してください。
            """

        # エージェントの実行（コンテキストを維持）
        result = Runner.run_sync(task_agent, query, context=context)

        print(f"エージェント: {result.final_output}")

        # 実行後のメモリストアの状態を表示（デバッグ用）
        print(f"\n現在のタスク状態:")
        for task in memory_store["tasks"]:
            status = "✓" if task["completed"] else "□"
            print(f"{status} [{task['id']}] {task['title']}")

        print("-" * 40)

    # 例として期待される出力：
    # 対話 1:
    # ユーザー: タスク一覧を表示してください。
    # エージェント: 現在のタスク一覧です：
    # 1. 買い物リスト作成 (完了)
    # 2. レポート提出 (未完了)
    # 3. 会議の準備 (未完了)
    #
    # 対話 2:
    # ユーザー: 新しいタスク「プレゼン資料作成」を追加してください。
    # エージェント: 「プレゼン資料作成」というタスクを追加しました。タスクIDは4です。
    #
    # ...
    #
    # 対話 5:
    # ユーザー: 未完了のタスクだけを表示してください。
    # エージェント: 未完了のタスク一覧です：
    # 3. 会議の準備
    # 4. プレゼン資料作成
