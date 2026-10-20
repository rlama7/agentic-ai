import pytest

from src.exceptions import (
    LLMAuthenticationError,
    LLMError,
    LLMRateLimitError,
    LLMResponseError,
    LLMServiceError,
)


@pytest.mark.parametrize(
    "exception_class",
    [
        LLMAuthenticationError,
        LLMRateLimitError,
        LLMServiceError,
        LLMResponseError,
    ],
)
def test_llm_exceptions_inherit_from_base(
    exception_class: type[LLMError],
) -> None:
    error = exception_class("Test error")

    assert isinstance(error, LLMError)
    assert isinstance(error, RuntimeError)
    assert str(error) == "Test error"
