from sales_agent.agent import SalesAgent
from verification_agent.agent import VerificationAgent
from underwriting_agent.agent import UnderwritingAgent
from sanction_agent.agent import SanctionAgent


class MasterAgent:
    def __init__(self):
        self.sales_agent = SalesAgent()
        self.verification_agent = VerificationAgent()
        self.underwriting_agent = UnderwritingAgent()
        self.sanction_agent = SanctionAgent()

    def handle_message(self, message, user_data):
        # Initial greeting
        if not message:
            return "Hello! I can help you with personal loans."

        # Step 1: Sales qualification
        if "loan" in message.lower():
            sales_result = self.sales_agent.run(user_data)

            if not sales_result["interested"]:
                return "At the moment, you may not be eligible for our loan offers."

            # Step 2: KYC Verification
            verification_result = self.verification_agent.run(user_data)

            if not verification_result["verified"]:
                return "Please complete your KYC to proceed further."

            # Step 3: Risk assessment
            risk_result = self.underwriting_agent.run(user_data)

            # Step 4: Loan sanction
            sanction_result = self.sanction_agent.run(risk_result)

            return sanction_result["message"]

        return "I can assist you with personal loan inquiries."
