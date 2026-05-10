from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from checker import check_email, check_password
from scorer import calculate_risk

app = FastAPI()

# allow the react frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/scan")
def scan(email: str, password: Optional[str] = None):
    # check the email for breaches
    raw_breaches = check_email(email)
    
    if raw_breaches is None:
        raw_breaches = []

    # xposedornot returns names as a list inside the Name field sometimes
    # we flatten everything into clean individual breach objects
    formatted_breaches = []
    for breach in raw_breaches:
        name = breach.get("Name", "")
        if isinstance(name, list):
            # its a list of names, make one entry per name
            for n in name:
                formatted_breaches.append({
                    "Name": str(n).strip(),
                    "BreachDate": "unknown",
                    "DataClasses": []
                })
        else:
            formatted_breaches.append(breach)

    # check password only if provided
    pwned_count = None
    if password:
        pwned_count = check_password(password)
        if pwned_count == -1:
            pwned_count = 0

    # calculate risk score
    risk = calculate_risk(formatted_breaches, pwned_count or 0)

    return {
        "breach_count": len(formatted_breaches),
        "breaches": formatted_breaches,
        "password_pwned": pwned_count,
        "risk": risk
    }