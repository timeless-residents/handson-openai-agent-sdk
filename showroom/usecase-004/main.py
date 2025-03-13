# showroom/usecase-004/main.py
from agents import Agent, Runner
from dotenv import load_dotenv
from typing import List, Dict, Optional, Type, Any
import os
from pydantic import BaseModel, Field


# Load environment variables
load_dotenv()

# Set OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
from agents import set_default_openai_key

set_default_openai_key(openai_api_key)

# Output Types: エージェントからの応答を構造化データとして受け取るための機能
# Pydanticモデルを使用して出力の型を定義できます


# 商品レビューの構造化データモデル
class ProductReview(BaseModel):
    product_name: str = Field(description="レビュー対象の商品名")
    rating: int = Field(description="評価（1-5の整数）", ge=1, le=5)
    pros: List[str] = Field(description="商品の良い点のリスト")
    cons: List[str] = Field(description="商品の改善点のリスト")
    summary: str = Field(description="レビューの要約")
    recommendation: bool = Field(description="他の人にお勧めするかどうか")


# 複数の商品比較の構造化データモデル
class ProductComparison(BaseModel):
    products: List[Dict[str, str]] = Field(description="比較する商品のリスト")
    comparison_points: List[str] = Field(description="比較ポイントのリスト")
    best_overall: str = Field(description="総合的に最も良い商品")
    best_value: str = Field(description="コストパフォーマンスが最も良い商品")
    comparison_table: Dict[str, Dict[str, str]] = Field(
        description="商品ごとの比較ポイント評価"
    )
    conclusion: str = Field(description="比較の結論")


if __name__ == "__main__":
    # 構造化データを返すエージェントの定義
    review_agent = Agent(
        name="Review Agent",
        instructions="""
        ユーザーの商品レビューリクエストに対して、詳細な構造化レビューを提供してください。
        以下の形式でJSON形式のレビューを返してください:
        {
            "product_name": "商品名",
            "rating": 評価（1-5の整数）,
            "pros": ["良い点1", "良い点2", ...],
            "cons": ["改善点1", "改善点2", ...],
            "summary": "レビューの要約",
            "recommendation": true/false（他の人にお勧めするかどうか）
        }
        """,
        model="o3-mini",
    )

    comparison_agent = Agent(
        name="Comparison Agent",
        instructions="""
        複数の商品を比較し、構造化された比較結果を提供してください。
        以下の形式でJSON形式の比較結果を返してください:
        {
            "products": [{"name": "商品名1"}, {"name": "商品名2"}, ...],
            "comparison_points": ["比較ポイント1", "比較ポイント2", ...],
            "best_overall": "総合的に最も良い商品",
            "best_value": "コストパフォーマンスが最も良い商品",
            "comparison_table": {
                "商品名1": {"比較ポイント1": "評価", "比較ポイント2": "評価", ...},
                "商品名2": {"比較ポイント1": "評価", "比較ポイント2": "評価", ...}
            },
            "conclusion": "比較の結論"
        }
        """,
        model="o3-mini",
    )

    print("【Usecase-004: Output Types の活用】")
    print("エージェントからの応答を構造化データとして受け取る例")
    print("-" * 40)

    # 商品レビューの例
    review_query = "新型スマートフォン「TechX Pro」のレビューを書いてください。"
    review_result = Runner.run_sync(review_agent, review_query)

    print("Query:", review_query)
    print("\n生のレスポンス:")
    print(review_result.final_output)

    # JSONレスポンスをパース
    import json
    import re

    # JSONを抽出するための正規表現パターン
    json_pattern = r"```json\s*(.*?)\s*```|({.*})"

    try:
        # まずJSONブロックを探す
        match = re.search(json_pattern, review_result.final_output, re.DOTALL)
        if match:
            json_str = match.group(1) if match.group(1) else match.group(2)
            review_json = json.loads(json_str)
        else:
            # 直接全体をJSONとして解析
            review_json = json.loads(review_result.final_output)

        review_data = ProductReview(**review_json)

        print("\n構造化レビュー結果:")
        print(f"商品名: {review_data.product_name}")
        print(f"評価: {review_data.rating}/5")
        print(f"良い点:")
        for pro in review_data.pros:
            print(f"- {pro}")
        print(f"改善点:")
        for con in review_data.cons:
            print(f"- {con}")
        print(f"要約: {review_data.summary}")
        print(f"推奨: {'はい' if review_data.recommendation else 'いいえ'}")
    except Exception as e:
        print(f"エラー: レビューデータの解析に失敗しました - {e}")
        # サンプルデータを表示
        print("\nサンプルデータを表示:")
        sample_review = ProductReview(
            product_name="TechX Pro",
            rating=4,
            pros=["高性能なカメラ", "長時間バッテリー", "美しいディスプレイ"],
            cons=["価格が高い", "充電速度が遅い"],
            summary="高性能だが価格が高いスマートフォン",
            recommendation=True,
        )
        print(f"商品名: {sample_review.product_name}")
        print(f"評価: {sample_review.rating}/5")
        print(f"良い点:")
        for pro in sample_review.pros:
            print(f"- {pro}")
        print(f"改善点:")
        for con in sample_review.cons:
            print(f"- {con}")
        print(f"要約: {sample_review.summary}")
        print(f"推奨: {'はい' if sample_review.recommendation else 'いいえ'}")
    print("-" * 40)

    # 商品比較の例
    comparison_query = "スマートフォン「TechX Pro」と「GalaxyS Ultra」と「iPhone Pro Max」を比較してください。"
    comparison_result = Runner.run_sync(comparison_agent, comparison_query)

    print("Query:", comparison_query)
    print("\n生のレスポンス:")
    print(comparison_result.final_output)

    # JSONレスポンスをパース
    try:
        # まずJSONブロックを探す
        match = re.search(json_pattern, comparison_result.final_output, re.DOTALL)
        if match:
            json_str = match.group(1) if match.group(1) else match.group(2)
            comparison_json = json.loads(json_str)
        else:
            # 直接全体をJSONとして解析
            comparison_json = json.loads(comparison_result.final_output)

        comparison_data = ProductComparison(**comparison_json)

        print("\n構造化比較結果:")
        print(f"比較商品:")
        for product in comparison_data.products:
            print(f"- {product.get('name', 'Unknown')}")
        print(f"比較ポイント:")
        for point in comparison_data.comparison_points:
            print(f"- {point}")
        print(f"総合評価最高: {comparison_data.best_overall}")
        print(f"コスパ最高: {comparison_data.best_value}")
        print(f"結論: {comparison_data.conclusion}")
    except Exception as e:
        print(f"エラー: 比較データの解析に失敗しました - {e}")
        # サンプルデータを表示
        print("\nサンプルデータを表示:")
        sample_comparison = ProductComparison(
            products=[
                {"name": "TechX Pro"},
                {"name": "GalaxyS Ultra"},
                {"name": "iPhone Pro Max"},
            ],
            comparison_points=["カメラ性能", "バッテリー寿命", "価格"],
            best_overall="iPhone Pro Max",
            best_value="GalaxyS Ultra",
            comparison_table={
                "TechX Pro": {
                    "カメラ性能": "良い",
                    "バッテリー寿命": "普通",
                    "価格": "高い",
                },
                "GalaxyS Ultra": {
                    "カメラ性能": "非常に良い",
                    "バッテリー寿命": "良い",
                    "価格": "普通",
                },
                "iPhone Pro Max": {
                    "カメラ性能": "最高",
                    "バッテリー寿命": "良い",
                    "価格": "非常に高い",
                },
            },
            conclusion="用途によって最適な選択は異なります",
        )
        print(f"比較商品:")
        for product in sample_comparison.products:
            print(f"- {product.get('name', 'Unknown')}")
        print(f"比較ポイント:")
        for point in sample_comparison.comparison_points:
            print(f"- {point}")
        print(f"総合評価最高: {sample_comparison.best_overall}")
        print(f"コスパ最高: {sample_comparison.best_value}")
        print(f"結論: {sample_comparison.conclusion}")

    # 例として期待される出力：
    # 構造化レビュー結果:
    # 商品名: TechX Pro
    # 評価: 4/5
    # 良い点:
    # - 高性能なカメラ
    # - 長時間バッテリー
    # - 美しいディスプレイ
    # 改善点:
    # - 価格が高い
    # - 充電速度が遅い
    # 要約: 高性能だが価格が高いスマートフォン
    # 推奨: はい
    #
    # 構造化比較結果:
    # 比較商品:
    # - TechX Pro
    # - GalaxyS Ultra
    # - iPhone Pro Max
    # 比較ポイント:
    # - カメラ性能
    # - バッテリー寿命
    # - 価格
    # 総合評価最高: iPhone Pro Max
    # コスパ最高: GalaxyS Ultra
    # 結論: 用途によって最適な選択は異なります
