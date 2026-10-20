class LLMError(RuntimeError):
    """Base exeception for LLM-related failures."""


class LLMAuthenticationError(LLMError):
    """Raised when API authentication or permission fail."""


class LLMRateLimitError(LLMError):
    """Raised when the provider rate limit is exceeded."""


class LLMServiceError(LLMError):
    """Raised when the LLM Servie is temporarily unavailable."""


class LLMResponseError(LLMError):
    """Raised when the LLM returns an invalid respone."""
