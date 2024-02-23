# config.py
class Classification_Config:
    max_tokens_per_minute = 40000
    model = "gpt-3.5-turbo-1106"
    temperature = 0.2
    max_tokens = 6

class Summarization_var_Config:
    max_tokens_per_minute=80000
    model = "gpt-3.5-turbo-1106"
    temperature=0.0
    max_tokens=500
    prompt_name= 'Prompt_summary_var'







class Summarization_Config:
    max_tokens_per_minute = 40000
    model = "gpt-3.5-turbo-1106"
    temperature = 0.1
    max_tokens = 500

class EntityRecognition_Config:
    max_tokens_per_minute = 20000
    model = "gpt-3.5-turbo-1106"
    temperature = 0.3
    max_tokens = 30
    prompt_name = 'Prompt_er'

class MultiClassification_Config:
    max_tokens_per_minute = 40000
    model = "gpt-3.5-turbo-1106"
    temperature = 0.2
    max_tokens = 10
    max_levels = 5