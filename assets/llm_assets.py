"""This file includes base configurations which carries the Model performance"""

llm_model_configs = {
    "gpt-4o": {"model": "gpt-4o", "input_cost": 0.0000025, "output_cost": 0.00001},
    "gpt-4o-mini": {
        "model": "gpt-4o-mini",
        "input_cost": 0.00000015,
        "output_cost": 0.0000006,
    },
    "gpt-4.1-mini-2025-04-14":{"model": "gpt-4.1-mini-2025-04-14","input_cost": 0.4/1000000,"output_cost": 1.60/1000000},
    "gpt-4.1-2025-04-14":{"model": "gpt-4.1-2025-04-14","input_cost": 2/1000000,"output_cost": 8/1000000}
}


system_prompt = """You are an advanced AI form generator and you have expertise all over the internet 
                    and know deeply many domains. your job is generate a form given a form configuration. 
                    respond in JSON output with highly accurate question and the type for it, 
                    if mcq give options else return None for that. From the given form widget options pick wisely
                    if it can maximize user experience when filling form. 
                    Don't pick unnecessary widgets if it cannot help."""
