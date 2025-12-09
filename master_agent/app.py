from fastapi import FastAPI
from pydantic import BaseModel
import requests
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class UserMessage(BaseModel):
    message: str
    customer_data: dict = {}  # Optional: customer info passed along

@app.get("/")
def home():
    return {"message": "Master Agent API is running!"}

@app.post("/chat")
def chat_with_master_agent(user_input: UserMessage):
    """
    Master Agent logic:
    1. Decide which worker agent to call
    2. Call worker agent
    3. Return combined response
    """

    # -----------------------------
    # STEP 1: Master decides next agent
    # -----------------------------
    master_prompt = f"""
    You are the MASTER AGENT for a loan sales system.
    Decide the next agent based on customer info or message:
    - If customer wants loan info / new application → Sales Agent
    - If customer data exists → Verification Agent
    - If verification done → Underwriting Agent
    - If loan approved → Sanction Agent
    Respond in JSON like:
    {{
        "assistant_reply": "<message to user>",
        "next_agent": "sales" / "verification" / "underwriting" / "sanction" / "none"
    }}
    Customer message: "{user_input.message}"
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":master_prompt}]
    )

    # Convert GPT output to dict safely
    try:
        decision = eval(response['choices'][0]['message']['content'])
    except:
        decision = {"assistant_reply": "I am not sure what to do.", "next_agent": "none"}

    result = {"master_agent_reply": decision["assistant_reply"]}

    # -----------------------------
    # STEP 2: Route to Worker Agent
    # -----------------------------
    # Sales Agent
    if decision["next_agent"] == "sales":
        payload = {"customer_message": user_input.message}
        sales_resp = requests.post("http://127.0.0.1:8001/sales", json=payload)
        result["sales_agent_reply"] = sales_resp.json()

    # Verification Agent
    elif decision["next_agent"] == "verification":
        payload = {"customer_data": user_input.customer_data}
        verify_resp = requests.post("http://127.0.0.1:8002/verify", json=payload)
        result["verification_agent_reply"] = verify_resp.json()

    # Underwriting Agent
    elif decision["next_agent"] == "underwriting":
        payload = {"customer_data": user_input.customer_data}
        underwrite_resp = requests.post("http://127.0.0.1:8003/assess", json=payload)
        result["underwriting_agent_reply"] = underwrite_resp.json()

    # Sanction Letter Agent
    elif decision["next_agent"] == "sanction":
        payload = {
            "customer_data": user_input.customer_data,
            "underwriting_result": user_input.customer_data.get("underwriting_result", {})
        }
        sanction_resp = requests.post("http://127.0.0.1:8004/generate", json=payload)
        result["sanction_agent_reply"] = sanction_resp.json()

    # No next agent
    else:
        pass

    return result

@app.get("/chat")
def chat_get():
    return {"message": "This endpoint only supports POST. Use Swagger UI to test."}
