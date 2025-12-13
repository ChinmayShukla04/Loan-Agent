class UnderwritingAgent:
    def run(self, user_data):
        credit_score = user_data.get("credit_score", 0)

        if credit_score >= 750:
            return {
                "risk": "LOW"
            }
        elif credit_score >= 650:
            return {
                "risk": "MEDIUM"
            }
        else:
            return {
                "risk": "HIGH"
            }
