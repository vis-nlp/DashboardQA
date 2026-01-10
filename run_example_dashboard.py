import os

import time

import subprocess

import argparse
 
from desktop_env.desktop_env import DesktopEnv

from mm_agents.agent import PromptAgent

from lib_run_single import run_single_example
 
# python run.py --observation_type screenshot --model gpt-4o-2024-11-20 --result_dir ./results_2

# API keys should be set as environment variables:
# export OPENAI_API_KEY=your_key_here
# export GENAI_API_KEY=your_key_here

# Time given for OS and dashboard setup  

print(" Waiting 5s for Ubuntu + browser + dashboard…")

time.sleep(5)
 
# DesktopEnv & GPT-4 Vision Agent initializaiton with a11y tree

env = DesktopEnv(
    headless=False,
    action_space="pyautogui",
    screen_size=(1920, 1080),
)
 
agent = PromptAgent(

    model="gemini-2.5-pro",
    action_space="pyautogui",
    observation_type="screenshot_a11y_tree", #"screenshot_a11y_tree", #"som",
    max_trajectory_length=3,

)
 
# Task setup
#"In the COVID-19 dashboard, click the Country Region dropdown caret to open the menu, "
#"then select “Afghanistan.”"

question = """
"Which county in the dashboard shows the greatest difference in poverty rates between ""Single-adult families"" and ""Families with married adults""?

A. Los Angeles County
B. San Diego County
C. Orange County
D. Alameda County"
"""
dashboard_url = "https://public.tableau.com/app/profile/public.policy.institute.of.california/viz/WhosinpovertyQ12023/Povertybydemographicgroupandregion" 
example = {
  "id": "tableau_dash_2_1",
  "snapshot": "chrome",
  "instruction": f"In this tableau dashboard, {question} Think step-by-step and output the final answer choice character only in this format <answer> final answer choice character </answer>", #"In this tableau dashbaord, I want you to select the year 2019 to display its data.",
  "source": dashboard_url, #"https://public.tableau.com/app/profile/victor.d.pr./viz/BeerConsumptionintheUS/Dashboard1", #"https://support.google.com/chrome/answer/95647?hl=en&ref_topic=7438325&sjid=16867045591165135686-AP#zippy=%2Cdelete-cookies-from-a-site",
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
os.makedirs(os.path.join("results", example["id"]), exist_ok=True)
args = argparse.Namespace(sleep_after_execution=1.0)

scores = []

run_single_example(

    agent,

    env,

    example,
    instruction=example["instruction"],

    args=args,

    example_result_dir=os.path.join("results", example["id"]),
    scores=scores,

    max_steps= 25,
    

)
 
print(f"✅ Finished; score = {scores[0]:.2f}")
 
