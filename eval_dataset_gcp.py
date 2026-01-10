import os

# API keys should be set as environment variables before running this script:
# export OPENAI_API_KEY=your_key_here
# export OPENAI_API_KEY_CUA=your_key_here  # For OpenAI CUA models
# export GENAI_API_KEY=your_key_here  # For Google GenAI
# export GEMINI_API_KEY=your_key_here  # For Gemini models
# export ANTHROPIC_API_KEY=your_key_here  # For Anthropic models
# export HF_TOKEN=your_key_here  # For HuggingFace datasets
# export GEMINI_ENDPOINT_URL=your_endpoint_url  # Optional: Gemini endpoint URL


import time
import subprocess
import argparse
from desktop_env.desktop_env import DesktopEnv

from mm_agents.agent import PromptAgent
from mm_agents.openai_cua_agent import OpenAICUAAgent
from mm_agents.jedi_3b_agent import JediAgent3B
from mm_agents.jedi_7b_agent import JediAgent7B
from mm_agents.uitars_agent import UITARSAgent

from mm_agents.gui_agents.s2.agents.agent_s import AgentS2
from mm_agents.gui_agents.s2.agents.grounding import OSWorldACI

from mm_agents.gat1_agent import GTA1Agent

from lib_run_single import run_single_example, run_single_example_openaicua
from datasets import load_dataset

from question_prompts import PROMPT_TEMPLATES

# Parse Command Line Arguments
parser = argparse.ArgumentParser(description="Parse model and setup names.")
parser.add_argument("--model-name", default="gemini-2.5-pro", type=str, help="Name of the model")
parser.add_argument("--setup-name", default="screenshot_a11y_tree", type=str, help="Name of the setup")
parser.add_argument("--dataset-name", default="ahmed-masry/DashboardQA-v0.2", type=str, help="Name of the HF dataset")
parser.add_argument("--results-folder", default="/home/ahmed_elmasry24653/results/", type=str, help="path of the results folder")

args = parser.parse_args()
results_path = args.results_folder

# Create DesktopEnv with docker and Ubuntu for GCP. 
env = DesktopEnv(
    provider_name="docker",
    os_type="Ubuntu",
    headless=True,
    action_space="pyautogui",
    screen_size=(1920, 1080),
)

# Create agent using the provided setup and model name
if args.model_name in ['computer-use-preview']:
    agent = OpenAICUAAgent(
        env=env,
        model=args.model_name,
        action_space="pyautogui",
        observation_type=args.setup_name, #"screenshot_a11y_tree", #"som",
        max_trajectory_length=3,
    )
elif args.model_name in ['jedi-3b']:
    agent = JediAgent3B(
        executor_model=args.model_name,
        action_space="pyautogui",
        observation_type=args.setup_name, #"screenshot_a11y_tree", #"som",
        max_steps=25
    )
elif args.model_name in ['jedi-7b']:
    agent = JediAgent7B(
        executor_model=args.model_name,
        action_space="pyautogui",
        observation_type=args.setup_name, #"screenshot_a11y_tree", #"som",
        max_steps=25
    )
elif args.model_name in ['UItars-7b']:
    agent = UITARSAgent(
        action_space="pyautogui",
        observation_type=args.setup_name, #"screenshot_a11y_tree", #"som",
        max_trajectory_length=25 # This is treated as max steps by Ui Tars
    )

elif args.model_name in ['GAT1-7b']:
    agent = GTA1Agent(
        platform="ubuntu",
        action_space="pyautogui",
        observation_type=args.setup_name, #"screenshot_a11y_tree", #"som",
        max_steps=25 # This is treated as max steps by Ui Tars
    )
    
elif args.model_name in ['S2']:

    engine_params = {
        "engine_type": "gemini",
        "model":"gemini-2.5-pro",
        "base_url": os.environ["GEMINI_ENDPOINT_URL"],
        "api_key": os.environ["GEMINI_API_KEY"],
    }


    grounding_height = None
    grounding_model_resize_width = 1366
    screen_height = 1080
    screen_width = 1920
    # If not provided, use the aspect ratio of the screen to compute the height
    if grounding_height is None:
        grounding_height = (
            screen_height
            * grounding_model_resize_width
            / screen_width
        )

    engine_params_for_grounding = {
        "engine_type": "gemini",
        "model": "gemini-2.5-pro",
        "grounding_width": grounding_model_resize_width,
        "grounding_height": grounding_height,
    }

    # NEW!
    grounding_agent = OSWorldACI(
        platform="linux",
        planner_model=engine_params,
        engine_params_for_grounding=engine_params_for_grounding,
        width=screen_width,
        height=screen_height,
    )

    # NEW!
    # change observation type name.
    observation_for_agent = args.setup_name
    if observation_for_agent == 'screenshot_a11y_tree':
      observation_for_agent = 'mixed'
    agent = AgentS2(
        engine_params,
        grounding_agent,
        platform="linux",
        action_space="pyautogui",
        observation_type=observation_for_agent,
        search_engine=None, #"Perplexica",
        memory_root_path=os.getcwd(),
        memory_folder_name="kb_s2",
        kb_release_tag="v0.2.2",
        embedding_engine_type="openai",
    )
else:
    agent = PromptAgent(
        model=args.model_name,
        action_space="pyautogui",
        observation_type=args.setup_name, #"screenshot_a11y_tree", #"som",
        max_trajectory_length=3,
    )
  
# Load HF dataset
test_dataset = load_dataset(args.dataset_name)['train'] #.select(range(3)) #TODO: Remove the select

# Iterate the dataset and get results. 
for row in test_dataset: 
    question = row['Question'] 
    row_id = str(row['row_id'])
    dashboard_urls = row['Tableau Dashboard']
    question_type = row['Question Type']
    question_template = PROMPT_TEMPLATES[question_type]
    formatted_question = question_template.format(question=question)
    
    # Results folder
    example_output_path = os.path.join(results_path, row_id)
    os.makedirs(example_output_path, exist_ok=True)

    example = {
      "id": row_id,
      "snapshot": "chrome",
      "instruction": formatted_question,
      "source": dashboard_urls,
      "config": [
        {
          "type": "launch",
          "parameters": {
            "command": [
              "google-chrome",
              "--remote-debugging-port=1337",
              "--start-fullscreen"
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
            "urls_to_open": dashboard_urls
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
    task_args = argparse.Namespace(sleep_after_execution=1.0)
    scores = []
    if args.model_name in ['computer-use-preview']:
        run_single_example_openaicua(
          agent,
          env,
          example,
          instruction=example["instruction"],
          args=task_args,
          example_result_dir=example_output_path,
          scores=scores,
          max_steps=25,
        )
    else:
        run_single_example(
          agent,
          env,
          example,
          instruction=example["instruction"],
          args=task_args,
          example_result_dir=example_output_path,
          scores=scores,
          max_steps=25,
        )

    print(f"Finished {row_id}; score = {scores[0]:.2f}")
 
