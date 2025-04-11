from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel


def get_usage_cost(completion_config, model_config):
    inp_tokens = completion_config.prompt_tokens
    out_tokens = completion_config.completion_tokens

    total_cost = (inp_tokens * model_config["input_cost"]) + (
        out_tokens * model_config["output_cost"]
    )
    return round(total_cost, 4)


class QuestionType(Enum):
    SHORT_ANSWER = "short_answer"
    PARAGRAPH = "paragraph"
    MULTIPLE_CHOICE_SINGLE = "multiple_choice_single"
    MULTIPLE_CHOICE_MULTI = "multiple_choice_multi"
    DROPDOWN = "dropdown"
    DATE = "date"
    TIME = "time"
    RATING = "rating"
    YES_NO = "yes_no"
    LIKERT = "likert"
    FILE_UPLOAD = "file_upload"
    NUMERIC = "numeric"
    EMAIL = "email"
    PHONE = "phone"
    ADDRESS = "address"


class FormModel(BaseModel):
    question_text: str
    question_type: QuestionType
    is_required: bool
    options: Optional[List[str]] = None


class Form(BaseModel):
    questions_list: List[FormModel]


def parse_results(response_out: Form):
    outputs_final = {"questions": []}
    questions_generated = response_out.questions_list
    for q in questions_generated:
        q = q.model_dump()
        q["question_type"] = q["question_type"].value
        outputs_final["questions"].append(q)
    return outputs_final
