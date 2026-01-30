# logic.py

def assess_risk(clause_text):
    text = clause_text.lower()
    if "terminate" in text and "any time" in text:
        return "High", "Unilateral termination without notice"
    if "penalty" in text:
        return "Medium", "Financial penalty clause"
    return "Low", "Standard contractual clause"


def explain_clause_simple(clause_text, risk_level):
    if risk_level == "High":
        return "This clause allows sudden termination without notice."
    if risk_level == "Medium":
        return "This clause imposes a financial penalty."
    return "This is a standard clause with low risk."


def overall_contract_risk(results):
    risks = [r["risk_level"] for r in results]
    if "High" in risks:
        return "High"
    if "Medium" in risks:
        return "Medium"
    return "Low"


def final_advice(overall_risk):
    if overall_risk == "High":
        return "Renegotiation is strongly recommended."
    if overall_risk == "Medium":
        return "Review penalty and obligation clauses carefully."
    return "Contract appears low risk."


def mock_ai_response(clause_text, risk_level):
    if risk_level == "High":
        return {
            "explanation": "Sudden termination may harm business stability.",
            "suggested_alternative": "Either party may terminate with 30 days notice."
        }
    if risk_level == "Medium":
        return {
            "explanation": "Penalty could affect cash flow.",
            "suggested_alternative": "Cap penalty to a reasonable amount."
        }
    return {
        "explanation": "Clause is generally safe.",
        "suggested_alternative": "No change required."
    }
