import json
import os
from typing import Any, Dict, Tuple

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI, OpenAI
from starlette.middleware.base import BaseHTTPMiddleware

from assets.llm_assets import llm_model_configs, system_prompt
from utils.model_utils import Form, get_usage_cost, parse_results

load_dotenv()
OPENAI_KEY = os.environ.get("OPENAI_KEY")
client = AsyncOpenAI(api_key=OPENAI_KEY)
config = llm_model_configs["gpt-4.1-mini-2025-04-14"]
# input_data = json.load(open("assets/input_dummy.json","r"))["dummy_input_configuration"]

app = FastAPI()

origins = [
    # "http://localhost",
    # "http://localhost:3000",
    "https://theform.ai/",
    "https://theformai.vercel.app/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Be more specific if needed
    allow_headers=["*"],
)


class LimitRequestSizeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_body_size: int = 1024 * 1024):  # 1 MB
        super().__init__(app)
        self.max_body_size = max_body_size

    async def dispatch(self, request: Request, call_next):
        body = await request.body()
        if len(body) > self.max_body_size:
            raise HTTPException(status_code=413, detail="Request too large")
        return await call_next(request)


app.add_middleware(LimitRequestSizeMiddleware)


@app.get("/")
async def root():
    return {"message": "Status active"}


@app.post("/get_form/")
async def get_form_completion(input_data: Dict[str, Any]):
    completion = await client.beta.chat.completions.parse(
        model=config["model"],
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"here is your form configuration: {input_data}",
            },
        ],
        response_format=Form,
    )
    llm_raw_out = completion.choices[0].message.parsed
    llm_processed_out = parse_results(llm_raw_out)
    token_charge = get_usage_cost(
        completion_config=completion.usage, model_config=config
    )
    llm_processed_out["cost"] = token_charge
    llm_processed_out["model_id"] = config["model"]
    return llm_processed_out
