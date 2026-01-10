from mm_agents.agent import PromptAgent
import os 

# API key should be set as environment variable: export OPENAI_API_KEY=your_key_here

agent = PromptAgent(
    model="gpt-4-vision-preview",
    observation_type="screenshot",
)
agent.reset()
# say we have an instruction and observation
instruction = "Please help me to find the nearest restaurant."
obs = {"screenshot": open("observation.jpg", 'rb').read()}
response, actions = agent.predict(
    instruction,
    obs
)