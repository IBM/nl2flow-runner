token_limits = {"gpt-4": 8192, "gpt-3.5-turbo": 4096, "davinci": 2049}
token_prompt_limits = {key: value - 100 for key, value in token_limits.items()}
token_length_plan = 100
