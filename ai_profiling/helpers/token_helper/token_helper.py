from ai_profiling.helpers.token_helper.token_helper_variables import token_prompt_limits


def get_revised_model_name(model_name: str) -> str:
    return "davinci" if "davinci" in model_name else model_name[:]


def get_token_length(model_name: str, input: str) -> int:
    return 0


def is_token_size_small_enough(model_name: str, input: str) -> bool:
    return (token_prompt_limits[get_revised_model_name(model_name)] - get_token_length(model_name, input)) >= 0
