# # summarization_var.py

import os
from socket import timeout
from dotenv import load_dotenv
from .utilities import log_info, log_error, handle_errors, OpenAIRequestError, TokenLimitError
from Summary_engine.prompts import classificaton_prompts
from tenacity import retry, stop_after_attempt, wait_exponential
import aiohttp
import asyncio
import json
import logging
import time
from config import Summarization_var_Config  
from preprocessing.prompt_count import TokenCounter
from aiohttp import ClientSession, ClientResponseError
from aiohttp.client_exceptions import ClientError
from aiohttp.web import HTTPException
from async_timeout import timeout as ClientTimeout


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class RateLimiter:
    def __init__(self):
        self.tokens_used = 0
        self.last_reset_time = time.time()

    def reset_tokens(self):
        self.tokens_used = 0
        self.last_reset_time = time.time()

    async def wait_for_token_availability(self, tokens_to_add):
        max_tokens_per_minute = Summarization_var_Config.max_tokens_per_minute
        elapsed_time = time.time() - self.last_reset_time

        if elapsed_time > 60:
            self.reset_tokens()

        if self.tokens_used + tokens_to_add > max_tokens_per_minute:
            wait_time = 60 - elapsed_time
            log_info(f"Approaching rate limit, will wait for {wait_time:.2f} seconds.")
            await asyncio.sleep(max(0, wait_time))
            self.reset_tokens()
        else:
            self.tokens_used += tokens_to_add

class OpenAIAPI:
    @staticmethod
    @handle_errors
    async def request_openai_api(model, messages):
        async with aiohttp.ClientSession() as session:
            url = 'https://api.openai.com/v1/chat/completions'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {OPENAI_API_KEY}'
            }
            payload = {
                'model': model,
                'messages': messages,
                'temperature': Summarization_var_Config.temperature,
                'max_tokens': Summarization_var_Config.max_tokens
            }

            try:
                timeout = aiohttp.ClientTimeout(total=60)
                async with session.post(url, headers=headers, json=payload, timeout=timeout) as resp:
                    resp.raise_for_status()  # Raises exception for 4xx/5xx responses
                    data = await resp.json()
                    return data['choices'][0]['message']['content']
            except ClientResponseError as e:
                raise OpenAIRequestError(e.status, f"OpenAI API HTTP error: {e.status} {e.message}")
            except ClientTimeout:
                log_error("OpenAI API request timed out")
                return None  # Or consider raising a custom timeout exception
            except ClientError as e:
                log_error(f"OpenAI API client error: {str(e)}")
                return None  # Or consider raising a custom client error exception
            except Exception as e:
                log_error(f"Unexpected error during OpenAI API request: {str(e)}")
                return None  # Or consider re-raising the exception after logging

                    
class Summarizer_var:
    def __init__(self):
        self.rate_limiter = RateLimiter()

    @handle_errors
    async def process_description(self, description, **kwargs):
        temperature = kwargs.get('temperature', Summarization_var_Config.temperature)
        model = kwargs.get('model', Summarization_var_Config.model)
        description_tokens = TokenCounter.count_tokens(description)

        log_info(f"Started processing description")

        await self.rate_limiter.wait_for_token_availability(description_tokens)
        prompt = classificaton_prompts[Summarization_var_Config.prompt_name](kwargs.get("points_words"),kwargs.get("Summary_type"),kwargs.get("importance"),kwargs.get("exclude"), kwargs.get("additional_info"))
        print(prompt)
        print(f"Prompt content: {classificaton_prompts.get(Summarization_var_Config.prompt_name, 'Prompt not found')}")

        messages = [
            {'role': 'system', 'content': prompt},
            {'role': 'user', 'content': description}]
        
        return await OpenAIAPI.request_openai_api(model, messages)






# ------------------------------------
# import os
# from dotenv import load_dotenv
# from .utilities import log_function_execution, log_info, log_error
# from classification_engine.prompts import classificaton_prompts
# from tenacity import retry, stop_after_attempt, wait_exponential
# import aiohttp
# import asyncio
# import json
# import logging
# import time
# from config import Summarization_var_Config  
# from preprocessing.prompt_count import TokenCounter

# load_dotenv()

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# class Summarizer_var:
#     tokens_used = 0
#     last_reset_time = time.time()
#     rate_limit_queue = asyncio.Queue()

#     @classmethod
#     async def wait_for_token_availability(cls, tokens_to_add):
#         max_tokens_per_minute = Summarization_var_Config.max_tokens_per_minute
#         elapsed_time = time.time() - cls.last_reset_time

#         if elapsed_time > 60:
#             cls.tokens_used = 0
#             cls.last_reset_time = time.time()

#         if cls.tokens_used + tokens_to_add > max_tokens_per_minute:
#             wait_time = 60 - elapsed_time
#             log_info(f"Approaching rate limit, will wait for {wait_time:.2f} seconds.")
#             await asyncio.sleep(max(0, wait_time))
#             cls.last_reset_time = time.time()
#             cls.tokens_used = tokens_to_add
#         else:
#             cls.tokens_used += tokens_to_add

#     @staticmethod
#     @log_function_execution
#     async def get_summarized_var_description(description, **kwargs):
#         temperature = kwargs.get('temperature', Summarization_var_Config.temperature)
#         model = kwargs.get('model', Summarization_var_Config.model)
#         description_tokens = int(len(description) / 3.5) + (1 if len(description) % 3.5 > 0 else 0)

#         log_info(f"Started processing description")

#         await Summarizer_var.wait_for_token_availability(description_tokens)
#         prompt = classificaton_prompts[Summarization_var_Config.prompt_name](kwargs.get("words"),kwargs.get("pointers"),kwargs.get("importance"),kwargs.get("exclude"), kwargs.get("additional_info"))
#         print(prompt)
#         print(f"Prompt content: {classificaton_prompts.get(Summarization_var_Config.prompt_name, 'Prompt not found')}")

#         messages = [
#             {'role': 'system', 'content': prompt},
#             {'role': 'user', 'content': description}]
        
#         async with aiohttp.ClientSession() as session:
#             url = 'https://api.openai.com/v1/chat/completions'
#             headers = {
#                 'Content-Type': 'application/json',
#                 'Authorization': f'Bearer {OPENAI_API_KEY}'
#             }
#             payload = {
#                 'model': model,
#                 'messages': messages,
#                 'temperature': Summarization_var_Config.temperature,
#                 'max_tokens': Summarization_var_Config.max_tokens
#             }

#             async with session.post(url, headers=headers, json=payload) as resp:
#                 if resp.status == 200:
#                     data = await resp.json()
#                     return data['choices'][0]['message']['content']
#                 else:
#                     response_text = await resp.text()
#                     log_error(f"OpenAI API error: {resp.status} {response_text}")
#                     return None