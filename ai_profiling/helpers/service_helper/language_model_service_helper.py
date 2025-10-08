from copy import deepcopy
from datetime import timedelta
import json
from typing import Any, Dict, List, Optional, Tuple, Union
from ai_profiling.helpers.service_helper.language_model_service_datatype import (
    MODEL_ID_RESOURCE_DICT,
    LLM_SERVICE_BASE_URL,
    LLM_SERVICE_COMPLETION_RESOURCE,
    LlmResponse,
)
import numpy as np
import requests


# chat_service
chat_service_url = "http://127.0.0.1:11434/api/chat"
chat_model_name = "dolphin-mixtral"


def get_perplexity(log_probs: List[float]) -> float:
    return float(np.exp(-1 * sum(log_probs) / len(log_probs)))


def get_openai_payload(
    prompts: List[str],
    id_model: str,
    temperature: float = 0.0,
    n: int = 1,
    max_tokens: int = 3000,
    min_tokens: int = 1,
    seed: int = 123456,
) -> Dict[str, Any]:
    return {
        "model": id_model,
        "prompt": prompts,
        "best_of": 0,
        "echo": False,
        "frequency_penalty": 0,
        "max_tokens": max_tokens,
        "n": n,
        "presence_penalty": 0,
        "seed": seed,
        "stop": "string",
        "stream": False,
        "temperature": temperature,
        "top_p": 1,
        "user": "string",
        "use_beam_search": False,
        "top_k": -1,
        "min_p": 0,
        "repetition_penalty": 1,
        "length_penalty": 1,
        "stop_token_ids": [0],
        "include_stop_str_in_output": False,
        "ignore_eos": False,
        "min_tokens": min_tokens,
        "skip_special_tokens": True,
        "spaces_between_special_tokens": True,
        "add_special_tokens": True,
        "response_format": {
            "type": "text",
            "json_schema": {
                "name": "string",
                "description": "string",
                "schema": {},
                "strict": True,
            },
        },
    }


def get_LLM_SERVICE_model_url(model_resource: str) -> str:
    url_elements = [LLM_SERVICE_BASE_URL, model_resource, LLM_SERVICE_COMPLETION_RESOURCE]
    return "/".join(url_elements)


def get_openai_api_headers(api_key: str) -> Dict[str, Any]:
    return {
        "accept": "application/json",
        "LLM_SERVICE_API_KEY": api_key,
        "Content-Type": "application/json",
    }


def get_response_from_post_request(
    obj: Dict[str, Any],
    url: str,
    headers: Optional[Dict[str, Any]] = None,
    timeout: int = 480,
) -> Tuple[Optional[Union[str, List[str]]], str, float]:
    text_response: Optional[Union[str, List[str]]] = None
    error_message: str = ""
    lag: Optional[timedelta] = None
    try:
        response = (
            requests.post(url, json=obj, timeout=timeout)
            if headers is None
            else requests.post(url, json=obj, headers=headers, timeout=timeout)
        )
        lag = response.elapsed
        payload = json.loads(response.text)

        if "response" in payload:  # single response from ollama
            text_response = payload["response"]
        elif "choices" in payload:  # multiple responses from LLM_SERVICE
            text_response = []
            for choice in payload["choices"]:
                if "text" in choice:
                    text_response.append(choice["text"])
    except Exception as e:
        error_message = str(e)
        print(error_message)

    return (
        text_response,
        error_message,
        (-1.0 if lag is None else lag.total_seconds()),
    )


def get_response_from_LLM_SERVICE(
    id_model: str,
    api_key: str,
    contents: List[str],
    max_tokens: int = 2000,
    min_tokens: int = 1,
    temperature: float = 0.0,
    n: int = 1,
    timeout: int = 480,
    seed: int = 123456,
) -> Tuple[Optional[Union[str, List[str]]], str, float]:
    resource_model = MODEL_ID_RESOURCE_DICT.get(id_model.lower(), "")
    if len(resource_model) == 0:
        raise Exception(f"RITZ model Resource for {id_model} is not found")

    return get_response_from_post_request(
        obj=get_openai_payload(
            prompts=deepcopy(contents),
            id_model=id_model[:],
            temperature=temperature,
            n=n,
            max_tokens=max_tokens,
            min_tokens=min_tokens,
            seed=seed,
        ),
        url=get_LLM_SERVICE_model_url(model_resource=resource_model),
        headers=get_openai_api_headers(api_key=api_key[:]),
        timeout=timeout,
    )


async def get_multiple_responses_from_LLM_SERVICE(
    id_model: str,
    api_key: str,
    content: str = "",
    temperature: float = 0.0,
    max_tokens: int = 3000,
    min_tokens: int = 1,
    num_generations: int = 1,
    verbose: bool = False,
    timeout: int = 480,
) -> List[LlmResponse]:
    text_response, error_message, lag = get_response_from_LLM_SERVICE(
        id_model=id_model,
        api_key=api_key,
        contents=[content],
        max_tokens=max_tokens,
        min_tokens=min_tokens,
        temperature=temperature,
        n=num_generations,
        timeout=timeout,
    )
    llm_responses: List[LlmResponse] = []
    if isinstance(text_response, list):
        for response in text_response:
            llm_responses.append(
                LlmResponse(
                    llm_model_id=id_model[:],
                    generated_text=response[:],
                    error_messages=([error_message] if len(error_message) > 0 else []),
                    lag=lag,
                )
            )
    if verbose:
        print("\nLLM responses:")
        print(llm_responses)
    return llm_responses


def get_response_from_local_chat_model(url: str, model_name: str, content: str = "") -> Any:
    obj = {
        "model": model_name,
        "messages": [{"role": "user", "content": content}],
        "stream": False,
    }
    response = requests.post(url, json=obj)
    payload = json.loads(response.text)
    if "message" in payload:
        if "content" in payload["message"]:
            return payload["message"]["content"]
    return ""
