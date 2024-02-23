import logging
import datetime
import os
import asyncio
import traceback
import tempfile

# Custom Exception Classes
class OpenAIRequestError(Exception):
    """Exception raised for errors during OpenAI API requests."""
    def __init__(self, status_code, message="OpenAI API request failed"):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

class TokenLimitError(Exception):
    """Exception raised when the token limit is exceeded."""
    def __init__(self, message="Token limit exceeded"):
        self.message = message
        super().__init__(self.message)

class InvalidInputError(ValueError):
    """Exception raised for invalid inputs to functions."""
    def __init__(self, message="Invalid input provided"):
        self.message = message
        super().__init__(self.message)

# Determine the appropriate temp directory
def get_temp_dir():
    if os.environ.get('AWS_EXECUTION_ENV') is not None:
        return '/tmp'
    else:
        return os.path.join(tempfile.gettempdir(), "your_app_name")

# Set up logging
log_file_name = f"{os.path.basename(__file__)[:-3]}_log.log"
log_file_path = os.path.join(get_temp_dir(), log_file_name)
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler(log_file_path), logging.StreamHandler()])

def log_error(message):
    logger = logging.getLogger(__name__)
    logger.error(f"{message}\n{traceback.format_exc()}")

def log_info(message):
    logger = logging.getLogger(__name__)
    logger.info(message)

# Error Handling Decorator
def handle_errors(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except OpenAIRequestError as e:
            log_error(f"Request error: {e.message}, Status Code: {e.status_code}")
        except TokenLimitError as e:
            log_error(e.message)
        except InvalidInputError as e:
            log_error(e.message)
        except Exception as e:
            log_error(f"Unexpected error: {str(e)}")
            raise
    return wrapper

async def log_async_error(message):
    logger = logging.getLogger(__name__)
    logger.error(f"{message}\n{traceback.format_exc()}")

async def log_async_function_execution(func, *args, **kwargs):
    logger = logging.getLogger(func.__name__)

    try:
        start_time = datetime.datetime.now()
        result = await func(*args, **kwargs)
        end_time = datetime.datetime.now()
        execution_time = end_time - start_time

        logger.info(f"Function {func.__name__} executed successfully")
        logger.info(f"Execution Time: {execution_time}")
        return result

    except Exception as e:
        logger.error(f"Error occurred in function {func.__name__}: {e}")
        raise

def log_function_execution(func):
    async def wrapper(*args, **kwargs):
        return await log_async_function_execution(func, *args, **kwargs)
    
    return wrapper


