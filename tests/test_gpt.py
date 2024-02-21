# built-in
import os
import unittest
import datetime
from unittest.mock import patch, MagicMock

# opneai
import openai

# ggpt
from ggpt.gpt import GPTClient
from ggpt.exception import InvalidAPIKeyError
from openai.types.chat import ChatCompletionMessage
from openai.types.chat.chat_completion import ChatCompletion, Choice


class TestGPTClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Set the OPENAI_API_KEY environment variable
        cls.api_key = "openai_api_key"
        os.environ["OPENAI_API_KEY"] = cls.api_key

        # Mock the openai.chat.completions.create method
        cls.mock_openai_patch = patch("openai.chat.completions.create")
        cls.mock_openai = cls.mock_openai_patch.start()

        cls.mock_openai.return_value = ChatCompletion(
            id="foo",
            model="gpt-4",
            object="chat.completion",
            choices=[
                Choice(
                    finish_reason="stop",
                    index=0,
                    message=ChatCompletionMessage(
                        content="Test response",
                        role="assistant",
                    ),
                )
            ],
            created=int(datetime.datetime.now().timestamp()),
        )

    def test_request_valid_key(self):
        # Given: GPTClient instance with a valid API key
        client = GPTClient(api_key=self.api_key)

        # When: `request` method is called
        response = client.request(prompt="Test request")

        # Then: Response should match the mocked response
        self.assertEqual(response.choices[0].message.content, "Test response")

    @patch("openai.chat.completions.create")
    def test_request_invalid_key(self, mock_openai):
        # Given: Mock `openai.chat.completions.create` raises an AuthenticationError
        client = GPTClient(api_key=f"{self.api_key}-invalid")
        mock_openai.side_effect = openai.AuthenticationError(message="Invalid API key", response=MagicMock(), body=MagicMock())

        # When: `request` method is called
        # Then: An InvalidAPIKeyError should be raised
        with self.assertRaises(InvalidAPIKeyError):
            client.request(prompt="Test request")

    def test_request_review(self):
        # Given: GPTClient instance with a valid API key
        client = GPTClient(api_key=self.api_key)

        # When: `request_review` method is called
        response = client.request_review(diff="Test request")

        # Then: Response should match the mocked response
        self.assertEqual(response, "Test response")

    def test_request_docstring(self):
        # Given: GPTClient instance with a valid API key
        client = GPTClient(api_key=self.api_key)

        # When: `request_docstring` method is called
        response = client.request_docstring(diff="Test request")

        # Then: Response should match the mocked response
        self.assertEqual(response, "Test response")

    def test_request_naming(self):
        # Given: GPTClient instance with a valid API key
        client = GPTClient(api_key=self.api_key)

        # When: `request_naming` method is called
        response = client.request_naming(user_prompt="Test request")

        # Then: Response should match the mocked response
        self.assertEqual(response, "Test response")
