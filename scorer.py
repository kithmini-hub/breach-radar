# these are data types we consider sensitive when calculating risk
# passwords and financial stuff are way worse than just an email being exposed
SENSITIVE_DATA_TYPES = [
    "Passwords",
    "Credit cards",
    "Bank account numbers",
    "Social security numbers",
    "Financial data",
    "Health records",
    "Private messages",
    "Phone numbers",
    "Physical addresses",
    "Passport numbers"
]

def calculate_risk(breaches: list, pwned_count: int) -> dict:
    # takes the breach list and password pwned count
    # returns a risk label + explanation + advice
    score = 0

    # factor 1: how many breaches was this email in
    breach_count = len(breaches) if breaches else 0
    if breach_count == 0:
        score += 0
    elif breach_count <= 2:
        score += 1
    elif breach_count <= 5:
        score += 2
    else:
        score += 3

    # factor 2: how sensitive was the data that got exposed
    if breaches:
        for breach in breaches:
            data_classes = breach.get("DataClasses", [])
            for sensitive in SENSITIVE_DATA_TYPES:
                if sensitive in data_classes:
                    score += 1
                    break  # only count once per breach, not for every sensitive field

    # factor 3: password exposure - this bumps the score up the most
    if pwned_count > 0:
        if pwned_count < 10:
            score += 2
        elif pwned_count < 100:
            score += 3
        else:
            score += 4  # if ur password leaked 100+ times its basically public lol

    # map final score to a risk level
    if score == 0:
        return {
            "label": "SAFE",
            "score": score,
            "explanation": "No breaches found and password is clean.",
            "advice": "You're good. Keep using unique passwords for each account."
        }
    elif score <= 2:
        return {
            "label": "LOW",
            "score": score,
            "explanation": f"Found in {breach_count} breach(es), but no highly sensitive data exposed.",
            "advice": "Consider changing passwords for affected accounts as a precaution."
        }
    elif score <= 5:
        return {
            "label": "MEDIUM",
            "score": score,
            "explanation": f"Found in {breach_count} breach(es) with moderately sensitive data.",
            "advice": "Change your passwords and enable 2FA on affected accounts immediately."
        }
    elif score <= 9:
        return {
            "label": "HIGH",
            "score": score,
            "explanation": f"Found in {breach_count} breach(es) with sensitive data exposed.",
            "advice": "Urgent: change passwords, enable 2FA, check for unauthorised account activity."
        }
    else:
        return {
            "label": "CRITICAL",
            "score": score,
            "explanation": f"Severe exposure — {breach_count} breaches, highly sensitive data, and/or widely leaked password.",
            "advice": "Immediate action needed: change all passwords, freeze credit if financal data was exposed, enable 2FA everywhere."
        }