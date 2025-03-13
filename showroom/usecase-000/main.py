from agents import Agent, Runner
from dotenv import load_dotenv
from agents import set_default_openai_key
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)

agent = Agent(
    name="Assistant", instructions="You are a helpful assistant", model="gpt-4o"
)

result = Runner.run_sync(
    agent,
    "Write the haiku about recursion in programming. Japanese language.",
)
print(result.final_output)
