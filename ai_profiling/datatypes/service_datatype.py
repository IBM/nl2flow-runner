from typing import Optional
from pydantic import BaseModel


class Seq2SeqDataModel(BaseModel):
    text: str = ""
    input: str = ""
    output: str = ""
    sample_hash: str = ""


class LLM_SERVICELlmTrainingDataModel(BaseModel):
    input: str = ""
    output: str = ""
    sample_hash: str = ""

    def get_seq2seq_data_model(self) -> Seq2SeqDataModel:
        return Seq2SeqDataModel(
            text=self.input + "\n" + self.output,
            input=self.input[:],
            output=self.output[:],
            sample_hash=self.sample_hash[:],
        )


class Seq2SeqEvaluationDataModel(BaseModel):
    text: str = ""
    input: str = ""
    output: str = ""
    response: str = ""
    sample_hash: str = ""
    llm_model_id: str = ""


class LocalLlmModel(BaseModel):
    llm_model: str = ""
    llm_model_url: Optional[str] = None
    tokenizer: str = ""
    tokenizer_url: Optional[str] = None
