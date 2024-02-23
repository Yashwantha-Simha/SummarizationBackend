import os
from dotenv import load_dotenv
from .utilities import log_function_execution, log_info, log_error
from Summary_engine.prompts import classificaton_prompts
from tenacity import retry, stop_after_attempt, wait_exponential
import aiohttp
import asyncio
import json
import logging
import time
from config import Classification_Config
from preprocessing.prompt_count import TokenCounter

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class Categorizer:
    tokens_used = 0
    last_reset_time = time.time()
    rate_limit_queue = asyncio.Queue()

    @classmethod
    async def maybe_wait_for_token_availability(cls, tokens_to_add):
        '''A class method to manage token availability the asynchronous process.
            Args:
            - tokens_to_add (int): The number of tokens to be added.

            The method checks the rate limit based on `max_tokens_per_minute` and waits if the token usage
            exceeds the limit. It tracks the time elapsed and resets the token count if a minute has passed.

            If token usage + `tokens_to_add` exceeds the `max_tokens_per_minute`, it waits until the end of
            the minute before retrying, ensuring the rate limit is not breached. If the rate limit is not exceeded,
            it adds the `tokens_to_add` to the count.

            Note:- Assumes `Classification_Config` contains the configuration including `max_tokens_per_minute`.
                 - Updates class attributes `tokens_used` and `last_reset_time` to manage token usage and reset times.
        '''
        max_tokens_per_minute = Classification_Config.max_tokens_per_minute
        elapsed_time = time.time() - cls.last_reset_time

        if elapsed_time > 60:
            cls.tokens_used = 0
            cls.last_reset_time = time.time()

        if cls.tokens_used + tokens_to_add > max_tokens_per_minute:
            # to wait until the end of the minute and then retrying
            wait_time = 60 - elapsed_time
            log_info(f"Approaching rate limit, will wait for {wait_time:.2f} seconds.")
            await asyncio.sleep(max(0, wait_time))
            cls.last_reset_time = time.time()
            # to Reset the token count after waiting
            cls.tokens_used = tokens_to_add  
        else:
            cls.tokens_used += tokens_to_add


    @staticmethod
    @log_function_execution
    async def get_categorized_description(description, **kwargs):
        '''
            Static method to categorize a given description using OpenAI's LLM model.
            This method prepares the description for categorization, checks token availability, and uses an asynchronous
            ClientSession to send a request to the OpenAI API for text completion. If successful (status code 200),
            it returns the categorized description. Otherwise, it logs the error and returns None.
            Args:
            - description (str): The text description to be categorized.
            - **kwargs (dict): Additional keyword arguments including:
                - 'prompt_name' (str): Name of the prompt to use (default: 'Prompt 1').
                - 'model' (str): Model to use for categorization (default: Classification_Config.model).
                - 'temperature' (float): Temperature for text generation (default: Classification_Config.temperature).
                - 'max_tokens' (int): Maximum tokens for text generation (default: Classification_Config.max_tokens).
            Returns:
            - str or None: Categorized description based on the model, or None if an error occurs.
        '''
        prompt_name = kwargs.get('prompt_name', 'Prompt 1')
        model = kwargs.get('model', Classification_Config.model)
        temperature = kwargs.get('temperature', Classification_Config.temperature)
        max_tokens = kwargs.get('max_tokens', Classification_Config.max_tokens)
        # Calculate tokens = 3.5 characters count as 1 token(approx)
        description_tokens = int(len(description) / 3.5) + (1 if len(description) % 3.5 > 0 else 0)

        log_info(f"Started processing description")

        await Categorizer.maybe_wait_for_token_availability(description_tokens)

        prompt = classificaton_prompts[prompt_name]
        print(prompt)

        messages = [
            {'role': 'system', 'content': prompt},
            {'role': 'user', 'content': description}]

        async with aiohttp.ClientSession() as session:
            url = 'https://api.openai.com/v1/chat/completions'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {OPENAI_API_KEY}'
            }
            payload = {
                'model': model,
                'messages': messages,
                'temperature': Classification_Config.temperature,
                'max_tokens': Classification_Config.max_tokens

            }
            async with session.post(url, headers=headers, json=payload) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data['choices'][0]['message']['content']
                    log_info(f"Classification result: {result}")
                    return result
                else:
                    response_text = await resp.text()
                    log_error(f"OpenAI API error: {resp.status} {response_text}")
                    return None

    





#1
# 
#  import os
# from openai import OpenAI
# from dotenv import load_dotenv
# from .utilites import log_function_execution
# from .prompts import classificaton_prompts
# from tenacity import retry, stop_after_attempt, wait_exponential

# load_dotenv()

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key=OPENAI_API_KEY)


# class Categorizer:
#     @staticmethod
#     @log_function_execution
#     @retry(
#         stop=stop_after_attempt(10),  # Number of retry attempts
#         wait=wait_exponential(multiplier=1, max=60),  # Exponential backoff settings
#     )
    
#     def get_categorized_description(description, prompt_name="Prompt 1", model="gpt-3.5-turbo-1106"):
#         prompt = classificaton_prompts[prompt_name]

#         messages = [
#             {'role': 'system', 'content': prompt},
#             {'role': 'user', 'content': description}
#         ]
#         response = client.chat.completions.create(
#             model=model,
#             messages=messages,
#             temperature=0.2,
#             max_tokens=6
#         )
#         return response.choices[0].message.content
