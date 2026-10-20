from unittest.mock import MagicMock, patch

import pytest

from src.exceptions import LLMResponseError
from src.llm_client import LLMClient


@pytest.mark.parametrize(
    "invalid_content",
    [
        "",
        "   ",
        None,
    ],
)
def test_generate_rejects_empty_content(
    invalid_content: str | None,
) -> None:
    with patch("src.llm_client.ai.Client") as mock_client_class:
        mock_client = mock_client_class.return_value

        mock_response = MagicMock()
        mock_response.choices[0].message.content = invalid_content

        mock_client.chat.completions.create.return_value = mock_response

        client = LLMClient()

        with pytest.raises(
            LLMResponseError,
            match="LLM returned an empty response",
        ):
            client.generate(
                prompt="Write an essay about AI.",
            )

        mock_client.chat.completions.create.assert_called_once()


def test_generate_returns_valid_response() -> None:
    # Arrange: Mock the external aisuite client
    with patch("src.llm_client.ai.Client") as mock_client_class:
        mock_client = mock_client_class.return_value

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Generated essay draft."

        mock_client.chat.completions.create.return_value = mock_response

        # Act: Execute the real LLMClient implementation
        client = LLMClient()

        result = client.generate(
            prompt="Write an essay about AI.",
            model="openai:gpt-4o",
            temperature=1.0,
        )

        # Assert: Verify the returned content
        assert result == "Generated essay draft."

        mock_client.chat.completions.create.assert_called_once_with(
            model="openai:gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": "Write an essay about AI.",
                }
            ],
            temperature=1.0,
        )


def test_generate_rejects_missing_choices() -> None:
    with patch("src.llm_client.ai.Client") as mock_client_class:
        mock_client = mock_client_class.return_value

        mock_response = MagicMock()
        mock_response.choices = []

        mock_client.chat.completions.create.return_value = mock_response

        client = LLMClient()

        with pytest.raises(
            LLMResponseError,
            match="LLM returned an invalid response structure",
        ):
            client.generate(
                prompt="Write an essay about AI.",
            )
