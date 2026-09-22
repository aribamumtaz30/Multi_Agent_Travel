"""LLM wrapper with transparent agent/tool observability."""
from __future__ import annotations
import json, time
from typing import Any
from openai import OpenAI, RateLimitError, APIError
from config.settings import get_settings

class LLMService:
    def __init__(self):
        self.settings=get_settings()
        self.client=OpenAI(api_key=self.settings.groq_api_key, base_url=self.settings.groq_base_url, timeout=self.settings.request_timeout_seconds) if self.settings.has_llm else None

    def generate_json(self, system_prompt:str, user_prompt:str, fallback:dict[str,Any], agent_name:str="Unknown Agent", state=None):
        trace = {"agent":agent_name,"llm_used":bool(self.client),"model":getattr(self.settings,'groq_model','offline'),"prompt_summary":user_prompt[:120],"result":"fallback"}
        if not self.client:
            if state is not None: state.setdefault('agent_trace',[]).append(trace)
            return fallback
        for attempt in range(3):
            try:
                response=self.client.chat.completions.create(model=self.settings.groq_model,messages=[{"role":"system","content":system_prompt},{"role":"user","content":user_prompt}],response_format={"type":"json_object"},temperature=0.2,max_tokens=2000)
                data=json.loads(response.choices[0].message.content or '{}')
                trace['result']='success'
                if state is not None: state.setdefault('agent_trace',[]).append(trace)
                return data if isinstance(data,dict) else fallback
            except RateLimitError:
                time.sleep(2**attempt)
            except (APIError,json.JSONDecodeError,TypeError,ValueError):
                break
        if state is not None: state.setdefault('agent_trace',[]).append(trace)
        return fallback
