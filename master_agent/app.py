# master_agent/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load .env variables first
load_dotenv()

# Initialize OpenAI client with API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

class UserMessage(BaseModel):
    message: str
    customer_data: dict | None = None

@app.get("/")
def home():
    return {"message": "Master Agent API is running!"}

@app.post("/chat")
def chat(user_input: UserMessage):
    result = {"master_agent_reply": None}

    try:
        master_prompt = f"""
You are the MASTER AGENT for a loan sales system.
Based on the customer's message and data, reply with a JSON object:
{{
  "assistant_reply": "<message to user>",
  "next_agent": "sales" / "verification" / "underwriting" / "sanction" / "none"
}}
Customer message: "{user_input.message}"
Customer data: {user_input.customer_data}
"""
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": master_prompt}]
        )

        content = resp.choices[0].message.content

        try:
            decision = eval(content)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Master Agent JSON parse error: {e}. Content: {content}"
            )

        result["master_agent_reply"] = decision.get("assistant_reply", "")
        next_agent = decision.get("next_agent", "none")

        if next_agent == "sales":
            sales_resp = requests.post(
                "http://127.0.0.1:8001/sales",
                json={"customer_message": user_input.message}
            )
            sales_resp.raise_for_status()
            result["sales_agent_reply"] = sales_resp.json()

        elif next_agent == "verification":
            if not user_input.customer_data:
                raise HTTPException(400, "No customer_data for verification")
            verify_resp = requests.post(
                "http://127.0.0.1:8002/verify",
                json={"customer_data": user_input.customer_data}
            )
            verify_resp.raise_for_status()
            result["verification_agent_reply"] = verify_resp.json()

        elif next_agent == "underwriting":
            if not user_input.customer_data:
                raise HTTPException(400, "No customer_data for underwriting")
            under_resp = requests.post(
                "http://127.0.0.1:8003/assess",
                json={"customer_data": user_input.customer_data}
            )
            under_resp.raise_for_status()
            result["underwriting_agent_reply"] = under_resp.json()

        elif next_agent == "sanction":
            if not user_input.customer_data:
                raise HTTPException(400, "No customer_data for sanction")
            sanction_resp = requests.post(
                "http://127.0.0.1:8004/generate",
                json={
                    "customer_data": user_input.customer_data,
                    "underwriting_result": user_input.customer_data.get("underwriting_result", {})
                }
            )
            sanction_resp.raise_for_status()
            result["sanction_agent_reply"] = sanction_resp.json()

        return result

    except HTTPException as he:
        raise he
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Internal error in Master Agent: {exc}"
        )
