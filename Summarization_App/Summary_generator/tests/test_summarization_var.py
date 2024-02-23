from unittest.mock import patch, AsyncMock
import pytest
from Summary_engine.summarization_var import OpenAIAPI

@pytest.mark.asyncio
async def test_request_openai_api_success():
    # Mock aiohttp.ClientSession().post() to return a successful response
    with patch('Summary_engine.summarization_var.aiohttp.ClientSession.post', new_callable=AsyncMock) as mocked_post:
        mocked_post.return_value.__aenter__.return_value.status = 200
        mocked_post.return_value.__aenter__.return_value.json = AsyncMock(return_value={"choices": [{"message": {"content": "Test response"}}]})
        
        response = await OpenAIAPI.request_openai_api("test-model", [{"test": "data"}])
        assert response == "Test response"
from unittest.mock import patch, AsyncMock
import pytest
from Summary_engine.summarization_var import OpenAIAPI
from aiohttp import ClientResponseError

@pytest.mark.asyncio
async def test_request_openai_api_http_error():
    # Mock aiohttp.ClientSession().post() to simulate an HTTP error
    with patch('Summary_engine.summarization_var.aiohttp.ClientSession.post', new_callable=AsyncMock) as mocked_post:
        mocked_post.return_value.__aenter__.side_effect = ClientResponseError(mocked_post.return_value, (), status=500)
        
        response = await OpenAIAPI.request_openai_api("test-model", [{"test": "data"}])
        assert response is None  # Assuming your error handling returns None in case of errors
