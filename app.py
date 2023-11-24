
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
from dotenv import load_dotenv
import os


# load environment variables from .env file
load_dotenv()

# Get the API key from the environment
API_KEY = os.getenv("OPENAI_API_KEY")
print(API_KEY)

USE_OPENAI = False

if USE_OPENAI:
    config_list = config_list_from_json(
        "OAI_CONFIG_LIST",
        filter_dict={
            "model": ["gpt-4", "gpt-4-0314", "gpt4", "gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-v0314"],
        },
    )

    config_list = [
        {
            'model': 'gpt-4-32k',
            'api_key': API_KEY,
        }
    ]
    llm_config={
        "seed": 42,  # seed for caching and reproducibility
        "config_list": config_list,  # a list of OpenAI API configurations
        "temperature": 0,  # temperature for sampling
    }
else:
    config_list = [
        {
            "api_base": "http://localhost:8000",
            "api_key": "NULL",
        }
    ]
    llm_config = {
        "request_timeout": 800,  # timeout for each request
        "seed": 42,  # seed for caching and reproducibility
        "config_list": config_list,  # a list of OpenAI API configurations
        "temperature": 0,  # temperature for sampling
    }


# create an AssistantAgent named "assistant"
assistant = AssistantAgent(
    name="assistant",
    llm_config=llm_config,  # configuration for autogen's enhanced inference API which is compatible with OpenAI API
)
# create a UserProxyAgent instance named "user_proxy"
user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,  # set to True or image name like "python:3" to use docker
    },
)
# the assistant receives a message from the user_proxy, which contains the task description
user_proxy.initiate_chat(
    assistant,
    # message="""What date is today? Compare the year-to-date gain for TWLO and TESLA.""",
    message="""What is the name of the model you are based on?""",
)

# user_proxy.send(
#     recipient=assistant,
#     message="""Plot a chart of their stock price change YTD and save to stock_price_ytd.png.""",
# )

# followup of the previous question
# user_proxy.send(
#     recipient=assistant,
#     message="""Predict where TWLO will be in 3 months.""",
# )