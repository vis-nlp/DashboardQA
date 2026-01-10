
# "In this tableau dashboard, {question} Think step-by-step and 
# output the final answer choice character only in this format <answer> final answer choice character </answer>"

PROMPT_TEMPLATES = {
    "factoid": """You are given a factoid question about an interactive Tableau dashboard that you need to navigate to answer the question.
You need to think step-by-step, but your final answer should be a single word, number, or phrase. 
Do not generate units. But if numerical units such as million, m, billion, B, or K are required, use the exact notation shown in the dashboard.
Remember to navigate the dashboard, think step-by-step, and put the final answer between these brackets <answer> </answer>
Question: {question}""",

    "mcq": """You are given a question about an interactive Tableau dashboard along with different possible answers. You need to navigate the dashboard to select the correct answer from them.
You need to think step-by-step, but your final answer should be one of the options letters only (without any additional text). 
Remember to navigate the dashboard, think step-by-step, and put the final answer between these brackets <answer> </answer>. After you generate the final answer, you should also generate the "DONE" pyautogui command.
Question: {question}""",

    "hypothetical": """You are given a hypothetical question about an interactive Tableau dashboard that you need to navigate to answer the question.
You need to think step-by-step, but your final answer should be a single word, number, or phrase. 
Do not generate units. But if numerical units such as million, m, billion, B, or K are required, use the exact notation shown in the dashboard.
Remember to navigate the dashboard, think step-by-step, and put the final answer between these brackets <answer> </answer>
Question: {question}""",

    "multidashboard": """You are given a question about two interactive Tableau dashboards that are open in two tabs in the browser. You need to navigate them to answer the question.
You need to think step-by-step, but your final answer should be a single word, number, or phrase. 
Do not generate units. But if numerical units such as million, m, billion, B, or K are required, use the exact notation shown in the dashboard.
Remember to navigate the dashboard, think step-by-step, and put the final answer between these brackets <answer> </answer>
Question: {question}""",

    "conversational": """You are given a multi-turn conversation, and your job is to answer the final question based on the conversation history and the information in the provided interactive Tableau dashboard that you need to navigate.
You need to think step-by-step, but your final answer should be a single word, number, or phrase. 
Do not generate units. But if numerical units such as million, m, billion, B, or K are required, use the exact notation shown in the dashboard.
Remember to navigate the dashboard, think step-by-step, and put the final answer between these brackets <answer> </answer>
Question: {question}"""
}