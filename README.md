# Loan-Agent 
Agentic AI for NBFC Personal Loan Sales (EY Hackathon)

## Problem Statement
NBFCs want to improve their personal loan sales success rate using an AI-driven conversational approach.

## Solution Overview
Loan-Agent is an Agentic AI system where:
- A Master Agent handles customer conversations
- Worker Agents assist in verification, underwriting, and loan sanction
- The system simulates a human-like loan sales process

## Architecture
User → Master Agent → Worker Agents → Final Loan Decision

## Agents Used
- Master Agent – Conversation & orchestration
- Sales Agent – Lead qualification
- Verification Agent – KYC check
- Underwriting Agent – Risk assessment
- Sanction Agent – Loan approval

## Tech Stack
- Python
- FastAPI
- Agent-based architecture
- Docker

## How to Run
```bash
pip install -r requirements.txt
uvicorn master_agent.app:app --reload
