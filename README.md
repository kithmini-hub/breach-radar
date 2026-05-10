# breach-radar

A Python CLI tool that checks if your email or password has been exposed in known data breaches.

Built on the [HaveIBeenPwned](https://haveibeenpwned.com) API — the same service used by Firefox, 1Password, and governments worldwide.

---

## Features

- Check any email against thousands of known breach databases
- Check passwords safely using **k-anonymity** — your password is never transmitted
- Risk scoring based on number of breaches, data sensitivity, and password exposure
- Clean terminal output with actionable advice

## How the password check works (k-anonymity)

Your password is never sent to any server. Instead:

1. The password is SHA-1 hashed locally on your machine
2. Only the first 5 characters of the hash are sent to the API
3. The API returns all hashes matching that prefix
4. Your device checks locally whether your full hash is in the list

The server never sees enough information to reconstruct what you're checking.

---

## Setup

```bash
git clone https://github.com/kithmini-hub/breach-radar
cd breach-radar
pip install -r requirements.txt
```

Get a free API key at [haveibeenpwned.com/API](https://haveibeenpwned.com/API/Key) and create a `.env` file:


HIBP_API_KEY=your_key_here

---

## Usage

```bash
# check email only
python main.py --email yourname@example.com

# check email + password
python main.py --email yourname@example.com --password yourpassword
```

---

## Stack

- Python 3.10+
- `requests` — API calls
- `typer` — CLI interface
- `python-dotenv` — API key management

## Why I built this

An extension of the security thinking behind [Cloud Sentinel](https://github.com/kithmini-hub/CloudSentinel) — runtime threat detection at the cloud level. This applies the same idea at a personal scale: surface exposure you didn't know you had.