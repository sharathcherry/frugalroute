"""OpenAI-compatible provider layer.

Local (free) model + remote (paid) model behind one interface. The remote provider
is switchable via config.REMOTE_PROVIDER:
  - "fireworks" (default) : the hackathon-scored path (OpenAI-compatible endpoint)
  - "azure"               : Azure OpenAI (AzureOpenAI client; deployment name = model)
  - "openai"              : any other OpenAI-compatible endpoint

NOTE: for the AMD Track 1 submission use "fireworks" — that's what the credits fund
and what the scoring runs on. "azure" is for dev/testing and portfolio alignment.

In MOCK mode returns canned text + token counts (no network).
"""
import config
import tokens


def _mock_complete(messages, model, kind):
    prompt = messages[-1]["content"] if messages else ""
    if kind == "local":
        text = f"[local:{model}] draft answer to: {prompt[:60]}"
    else:
        text = f"[remote:{model}] high-quality answer to: {prompt[:60]}"
    return text, tokens.count(prompt), tokens.count(text)


def _remote_client_and_model(model):
    """Return (client, model_name) for the configured remote provider."""
    if config.REMOTE_PROVIDER == "azure":
        from openai import AzureOpenAI
        client = AzureOpenAI(
            azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
            api_key=config.AZURE_OPENAI_API_KEY,
            api_version=config.AZURE_OPENAI_API_VERSION,
        )
        return client, (model or config.AZURE_OPENAI_DEPLOYMENT)  # Azure: model = deployment name
    from openai import OpenAI
    client = OpenAI(base_url=config.REMOTE_BASE_URL, api_key=config.REMOTE_API_KEY)
    return client, (model or config.REMOTE_MODEL)


def complete(messages, kind="remote", model=None, base_url=None, api_key=None,
             max_tokens=None):
    """Return (text, prompt_tokens, completion_tokens).

    Args:
        kind:       'local' | 'remote'
        model:      override default model
        base_url:   override endpoint (local benchmarking)
        api_key:    override key (local benchmarking)
        max_tokens: cap generation length — important for local calls over the
                    network (prevents runaway slow responses). Default: None
                    (no cap) for remote, 400 for local via nodes.py.
    """
    default_model = config.LOCAL_MODEL if kind == "local" else config.REMOTE_MODEL
    if config.MOCK:
        return _mock_complete(messages, model or default_model, kind)

    kwargs = {"model": None, "messages": messages, "temperature": 0}
    if max_tokens is not None:
        kwargs["max_tokens"] = max_tokens

    if kind == "local":
        from openai import OpenAI
        client = OpenAI(base_url=base_url or config.LOCAL_BASE_URL,
                        api_key=api_key or config.LOCAL_API_KEY)
        kwargs["model"] = model or config.LOCAL_MODEL
    else:
        client, m = _remote_client_and_model(model)
        kwargs["model"] = m

    import time
    from openai import RateLimitError
    
    max_retries = 10
    for attempt in range(max_retries):
        try:
            r = client.chat.completions.create(**kwargs)
            u = r.usage
            return r.choices[0].message.content, u.prompt_tokens, u.completion_tokens
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise e
            print(f"Rate limited by Fireworks, waiting 30 seconds (attempt {attempt+1}/{max_retries})...")
            time.sleep(30)
