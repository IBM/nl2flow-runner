import os
from typing import List, Optional
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    # AutoProcessor,
    # GenerationConfig,
)

from ai_profiling.datatypes.service_datatype import LocalLlmModel
from ai_profiling.helpers.service_helper.language_model_service_datatype import LlmResponse

LLM_DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"
tokenizers_dict = {}
models_dict = {}
processors_dict = {}
HF_TOKEN = "HF_TOKEN"


def get_response_from_llm_with_tokenizer(
    input: str, model_obj: LocalLlmModel, temperature: float, max_tokens: int
) -> Optional[str]:
    if "tokenizer" not in model_obj or "model" not in model_obj:
        return None

    if HF_TOKEN in os.environ:
        if model_obj.tokenizer not in tokenizers_dict:
            tokenizers_dict[model_obj.tokenizer] = AutoTokenizer.from_pretrained(
                (model_obj.tokenizer_url if model_obj.tokenizer_url is not None else model_obj.tokenizer),
                token=os.getenv(HF_TOKEN, ""),
            )

        if model_obj.llm_model not in models_dict:
            models_dict[model_obj.llm_model] = AutoModelForCausalLM.from_pretrained(
                (model_obj.llm_model_url if model_obj.llm_model_url is not None else model_obj.llm_model),
                torch_dtype=torch.bfloat16 if "cuda" in LLM_DEVICE else torch.float16,
                device_map="auto",
                token=os.getenv(HF_TOKEN, ""),
            )
    else:
        if model_obj.tokenizer not in tokenizers_dict:
            tokenizers_dict[model_obj.tokenizer] = AutoTokenizer.from_pretrained(
                model_obj.tokenizer_url if model_obj.tokenizer_url is not None else model_obj.tokenizer
            )

        if model_obj.llm_model not in models_dict:
            models_dict[model_obj.llm_model] = AutoModelForCausalLM.from_pretrained(
                (model_obj.llm_model_url if model_obj.llm_model_url is not None else model_obj.llm_model),
                torch_dtype=torch.bfloat16 if "cuda" in LLM_DEVICE else torch.float16,
                device_map="auto",
            )

    tokenizer = tokenizers_dict[model_obj.tokenizer]
    model = models_dict[model_obj.llm_model]

    if max_tokens > tokenizer.model_max_length:
        max_tokens = tokenizer.model_max_length - 1

    input_tokens_dict = tokenizer(input, return_tensors="pt")
    input_tokens_dict = {k: v.to(model.device) for k, v in input_tokens_dict.items()}
    output = model.generate(**input_tokens_dict, do_sample=False, max_new_tokens=max_tokens)
    response = tokenizer.decode(
        output[0][len(input_tokens_dict["input_ids"][0]) :],  # noqa: E203
        skip_special_tokens=True,
    )

    if response is not None and isinstance(response, str):
        print(f"response length is {len(response)}")

    return response


# def get_response_from_llm_with_pipeline(
#     input: str, model_obj: Dict[str, Any], temperature: float, max_tokens: int
# ) -> Optional[str]:
#     if "tokenizer" not in model_obj or "model" not in model_obj:
#         return None

#     if model_obj["tokenizer"] not in tokenizers_dict:
#         tokenizers_dict[model_obj["tokenizer"]] = AutoTokenizer.from_pretrained(
#             model_obj["tokenizer_url"] if "tokenizer_url" in model_obj else model_obj["tokenizer"]
#         )

#     if model_obj["model"] not in models_dict:
#         models_dict[model_obj["model"]] = transformers.pipeline(
#             "text-generation",
#             model=model_obj["model"],
#             torch_dtype=torch.float16,
#             device_map="auto",
#         )

#     tokenizer = tokenizers_dict[model_obj["tokenizer"]]

#     if max_tokens > tokenizer.model_max_length:
#         max_tokens = tokenizer.model_max_length - 1

#     pipeline = models_dict[model_obj["model"]]

#     sequences = pipeline(
#         input,
#         do_sample=False,
#         num_return_sequences=1,
#         eos_token_id=tokenizer.eos_token_id,
#         max_length=(len(input)) + max_tokens,
#     )

#     for seq in sequences:
#         response = seq["generated_text"]

#     return response


# def get_response_from_llm_with_vllm(
#     input: str, model_obj: Dict[str, Any], temperature: float, max_tokens: int
# ) -> Optional[str]:
#     if "tokenizer" not in model_obj or "model" not in model_obj:
#         return None

#     if model_obj["model"] not in models_dict:
#         models_dict[model_obj["model"]] = LLM(
#         model=model_obj["model"],
#         dtype="bfloat16"
#         )

#     sampling_params = SamplingParams(
#         temperature=0,
#         max_tokens=max_tokens
#     )

#     outputs = models_dict[model_obj["model"]].generate([input], sampling_params)

#     for output in outputs:
#         response = output.outputs[0].text
#         break

#     return response


# def get_response_from_llm_with_autoprocessor(
#     input: str, model_obj: Dict[str, str], temperature: float, max_tokens: int
# ) -> Optional[str]:
#     """
#     This function supports only cuda
#     """
#     if "model" not in model_obj:
#         return None

#     if model_obj["model"] not in processors_dict:
#         processors_dict[model_obj["model"]] = AutoProcessor.from_pretrained(model_obj["model"], trust_remote_code=True) # noqa: E501

#     if model_obj["model"] not in models_dict:
#         models_dict[model_obj["model"]] = AutoModelForCausalLM.from_pretrained(
#             model_obj["model"],
#             device_map="cuda",
#             torch_dtype="auto",
#             trust_remote_code=True,
#             _attn_implementation="flash_attention_2",
#         ).cuda()

#     processor = processors_dict[model_obj["model"]]
#     model = models_dict[model_obj["model"]]

#     # Load generation config
#     generation_config = GenerationConfig.from_pretrained(model_obj["model"])
#     inputs = processor(text=input, return_tensors="pt").to("cuda:0")
#     generate_ids = model.generate(
#         **inputs,
#         temperature=temperature,
#         max_new_tokens=max_tokens,
#         generation_config=generation_config,
#     )
#     generate_ids = generate_ids[:, inputs["input_ids"].shape[1] :]  # noqa: E203
#     response = processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

#     return response


def get_responses_from_local_llm(
    input_texts: List[str],
    model_obj: LocalLlmModel,
    temperature: float,
    max_tokens: int,
) -> List[LlmResponse]:
    error_messages: List[str] = []
    responses: List[LlmResponse] = []
    for input_text in input_texts:
        try:
            response = get_response_from_llm_with_tokenizer(
                input=input_text,
                model_obj=model_obj,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            if response is None:
                print("Response is None")
            else:
                print(f"Response length is {len(response)}")

            responses.append(
                LlmResponse(
                    llm_model_id=model_obj.llm_model[:],
                    generated_text=(response if response is not None else ""),
                    error_messages=error_messages,
                    lag=0.0,
                )
            )
        except Exception as e:
            print(e)
            model_name = model_obj["model"] if "model" in model_obj else "default_model"
            error_message = str(e)
            print(f"Error in response retrieval: {error_message}")
            error_messages.append(f"Error message from local LLM {model_name}: {error_message}")

    return responses
