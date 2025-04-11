from enum import Enum
from pydantic import BaseModel
from typing import Dict, Any, Union, List, Optional, Tuple


def get_usage_cost(completion_config,model_config):
    inp_tokens = completion_config.prompt_tokens
    out_tokens = completion_config.completion_tokens

    total_cost = (inp_tokens*model_config["input_cost"])+(out_tokens*model_config["output_cost"])
    return round(total_cost,4)


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


async def get_tailored_form(client:Any,
                      config: Dict[str,Any],
                      system_prompt: str, 
                      input_data: Dict[str,Any]) -> Tuple[Form, float]:
    completion = await client.beta.chat.completions.parse(model=config["model"],
                                                    messages=[{"role": "system", "content": system_prompt},
                                                              {"role": "user", "content": f"here is your form configuration: {input_data}"},],
                                                    response_format=Form,)
    # response_out = completion.choices[0].message.parsed
    # per_request_cost = get_usage_cost(completion_config=completion.usage,
    #                                   model_config=config)

    return completion

def parse_results(response_out: Form):
    outputs_final = {"questions":[]}
    questions_generated = response_out.questions_list
    for q in questions_generated:
        q = q.model_dump()
        q["question_type"] = q["question_type"].value
        outputs_final["questions"].append(q)
    return outputs_final