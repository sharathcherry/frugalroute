window.DATA = {
  "engine": "langgraph",
  "records": [
    {
      "id": "s1",
      "task": "Classify the sentiment of: 'I love this product, works great!'",
      "answer": "[local:qwen2.5:3b-instruct] draft answer to: Classify the sentiment of: 'I love this product, works great",
      "category": "classification",
      "source": "local",
      "route_p": 0.28,
      "confidence": 0.9,
      "remote_tokens": 0,
      "tokens_saved": 0
    },
    {
      "id": "s2",
      "task": "Summarize: The quarterly report showed revenue growth of 12 percent driven by cloud.",
      "answer": "[local:qwen2.5:3b-instruct] draft answer to: Summarize: The quarterly report showed revenue growth of 12 ",
      "category": "summarization",
      "source": "local",
      "route_p": 0.29,
      "confidence": 0.9,
      "remote_tokens": 0,
      "tokens_saved": 0
    },
    {
      "id": "s3",
      "task": "Why does increasing temperature speed up a chemical reaction? Explain step by step.",
      "answer": "[remote:accounts/fireworks/models/llama-v3p1-8b-instruct] high-quality answer to: Why does increasing temperature speed up chemical reaction ?",
      "category": "reasoning",
      "source": "remote",
      "route_p": 0.89,
      "confidence": null,
      "remote_tokens": 48,
      "tokens_saved": 1
    },
    {
      "id": "s4",
      "task": "Extract all email addresses from: contact a@x.com or b@y.org today.",
      "answer": "[local:qwen2.5:3b-instruct] draft answer to: Extract all email addresses from: contact a@x.com or b@y.org",
      "category": "extraction",
      "source": "local",
      "route_p": 0.28,
      "confidence": 0.9,
      "remote_tokens": 0,
      "tokens_saved": 0
    },
    {
      "id": "s5",
      "task": "Calculate the sum of 145 and 278.",
      "answer": "[remote:accounts/fireworks/models/llama-v3p1-8b-instruct] high-quality answer to: Calculate sum 145 278 .",
      "category": "math",
      "source": "remote",
      "route_p": 0.87,
      "confidence": null,
      "remote_tokens": 39,
      "tokens_saved": 3
    },
    {
      "id": "s6",
      "task": "What is the capital of France?",
      "answer": "[local:qwen2.5:3b-instruct] draft answer to: What is the capital of France?",
      "category": "qa",
      "source": "local",
      "route_p": 0.25,
      "confidence": 0.9,
      "remote_tokens": 0,
      "tokens_saved": 0
    },
    {
      "id": "s7",
      "task": "Explain step by step how HTTPS encrypts a web request.",
      "answer": "[remote:accounts/fireworks/models/llama-v3p1-8b-instruct] high-quality answer to: Explain step by step how HTTPS encrypts web request .",
      "category": "reasoning",
      "source": "remote",
      "route_p": 0.88,
      "confidence": null,
      "remote_tokens": 48,
      "tokens_saved": 1
    }
  ],
  "agg": {
    "n": 7,
    "remote_tokens": 135,
    "tokens_saved": 5,
    "free_pct": 57.1,
    "escalate_pct": 42.9,
    "cache_hits": 0,
    "mix": {
      "local": 4,
      "remote": 3
    },
    "by_category": {
      "classification": {
        "local": 1,
        "remote": 0,
        "cache": 0,
        "other": 0
      },
      "summarization": {
        "local": 1,
        "remote": 0,
        "cache": 0,
        "other": 0
      },
      "reasoning": {
        "local": 0,
        "remote": 2,
        "cache": 0,
        "other": 0
      },
      "extraction": {
        "local": 1,
        "remote": 0,
        "cache": 0,
        "other": 0
      },
      "math": {
        "local": 0,
        "remote": 1,
        "cache": 0,
        "other": 0
      },
      "qa": {
        "local": 1,
        "remote": 0,
        "cache": 0,
        "other": 0
      }
    }
  }
};
