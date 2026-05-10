from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from checker import check_email, check_password
from scorer import calculate_risk

app = FastAPI()

# allow the react frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # vite's default port
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/scan")
def scan(email: str, password: Optional[str] = None):
    # check the email for breaches
    breaches = check_email(email)
    
    if breaches is None:
        breaches = []

    # check password only if provided
    pwned_count = None
    if password:
        pwned_count = check_password(password)
        if pwned_count == -1:
            pwned_count = 0

    # calculate risk score
    risk = calculate_risk(breaches, pwned_count or 0)

    return {
        "breach_count": len(breaches),
        "breaches": breaches,
        "password_pwned": pwned_count,
        "risk": risk
    }