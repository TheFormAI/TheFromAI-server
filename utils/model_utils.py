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

class WidgetType(Enum):
    CHECKBOX = "checkbox"
    RADIO_GROUP = "radio_group"
    TOGGLE = "toggle"
    DATETIME = "datetime"
    FILE_DROPZONE = "file_dropzone"
    NUMERIC = "numeric"
    DECIMAL = "decimal"
    CURRENCY = "currency"
    PERCENT = "percent"
    URL = "url"
    COUNTRY_SELECT = "country_select"
    STATE_SELECT = "state_select"
    CITY_SELECT = "city_select"
    ZIP_CODE = "zip_code"
    COLOR_PICKER = "color_picker"
    SLIDER = "slider"
    SOCIAL_MEDIA = "social_media"
    TAGS = "tags"
    CAPTCHA = "captcha"
    LANGUAGE_SELECT = "language_select"
    TIMEZONE_SELECT = "timezone_select"
    RANKING = "ranking"
    OPINION_SCALE = "opinion_scale"
    STAR_RATING = "star_rating"
    EMOJI_RATING = "emoji_rating"


class FormModel(BaseModel):
    question_text: str
    question_type: QuestionType
    is_required: bool
    widget_type: Optional[Union[WidgetType,None]] = None
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
