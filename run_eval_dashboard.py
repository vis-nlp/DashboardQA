import os
import time
import subprocess
import argparse
from desktop_env.desktop_env import DesktopEnv
from mm_agents.agent import PromptAgent
from lib_run_single import run_single_example
import pandas as pd
from tqdm import tqdm

# python run.py --observation_type screenshot --model gpt-4o-2024-11-20 --result_dir ./results_2

# API keys should be set as environment variables:
# export OPENAI_API_KEY=your_key_here
# export GENAI_API_KEY=your_key_here

MODEL_NAME = "gemini-2.5-pro"
 
# DesktopEnv & GPT-4 Vision Agent initializaiton with a11y tree

env = DesktopEnv(
    headless=True,
    action_space="pyautogui",
    screen_size=(1920, 1080),
)
 
agent = PromptAgent(
    model=MODEL_NAME,
    action_space="pyautogui",
    observation_type="screenshot_a11y_tree", #"screenshot_a11y_tree", #"som",
    max_trajectory_length=3,

)
 
# Task setup

csv_df = pd.read_csv('mcq_dataset.csv')
for _, row in tqdm(csv_df.iterrows()):
    question = row['Question']
    dashboard_url = row['Tableau dashboard']
    row_id = str(row['row_id'])

    os.makedirs(os.path.join("models_results", MODEL_NAME, row_id), exist_ok=True)

    example = {
      "id": row_id,
      "snapshot": "chrome",
      "instruction": f"Navigate the provided Tableau dashboard to answer the following question: {question}. Think through the problem step by step, then provide only the final answer choice letter, X, in this format: <answer>X</answer>.", #"In this tableau dashbaord, I want you to select the year 2019 to display its data.",
      "source": dashboard_url,
      "config": [
        {
          "type": "launch",
          "parameters": {
            "command": [
              "google-chrome",
              "--remote-debugging-port=1337"
            ]
          }
        },
        {
          "type": "launch",
          "parameters": {
            "command": [
              "socat",
              "tcp-listen:9222,fork",
              "tcp:localhost:1337"
            ]
          }
        },
        {
          "type": "chrome_open_tabs",
          "parameters": {
            "urls_to_open": [
              dashboard_url
            ]
          }
        },
        {
          "type": "execute",
          "parameters": {
            "command": [
              "python",
              "-c",
              "import pyautogui; import time; pyautogui.click(1062, 345); time.sleep(0.5);"
            ]
          }
        }
      ],
      "trajectory": "trajectories/",
      "related_apps": [
        "chrome"
      ],
      "evaluator": {
        "func": "is_cookie_deleted",
        "result": {
          "type": "cookie_data",
          "dest": "Cookies"
        },
        "expected": {
          "type": "rule",
          "rules": {
            "type": "domains",
            "domains": [
              ".amazon.com"
            ]
          }
        }
      },
      "proxy": True
    }
# Task execution
    args = argparse.Namespace(sleep_after_execution=1.0)
    scores = []
    run_single_example(
        agent,
        env,
        example,
        instruction=example["instruction"],
        args=args,
        example_result_dir=os.path.join("models_results", MODEL_NAME, example["id"]),
        scores=scores,
        max_steps= 25,
    )
 
print(f"✅ Finished; score = {scores[0]:.2f}")
 
