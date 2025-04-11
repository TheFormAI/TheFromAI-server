import os
from fastapi import FastAPI
import json
from openai import OpenAI
from dotenv import load_dotenv

from utils.model_utils import (Form,get_usage_cost,get_tailored_form,
                               parse_results)
from assets.llm_assets import (llm_model_configs,
                               system_prompt)

from typing import Dict, Tuple, Any

load_dotenv()
OPENAI_KEY = os.environ.get("OPENAI_KEY")
client     = OpenAI(api_key=OPENAI_KEY)
config = llm_model_configs["gpt-4o"]
input_data = json.load(open("assets/input_dummy.json","r"))["dummy_input_configuration"]
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/get_form/")
async def get_form():
    result = await get_tailored_form(client=client, config=config,
                                                 system_prompt=system_prompt,
                                                 input_data=str(input_data))

    # response_final = parse_results(response_out=result)
    return result