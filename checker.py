import hashlib
import requests
import os
from dotenv import load_dotenv

# loads the .env file so we can grab the api key
load_dotenv()

HIBP_API_KEY = os.getenv("HIBP_API_KEY")

# hibp requires these headers with every request or it rejects us
HIBP_HEADERS = {
    "hibp-api-key": HIBP_API_KEY,
    "user-agent": "breach-radar-cli"
}

def check_email(email: str) -> list:
    # hits the hibp api and checks if this email showed up in any breaches
    # returns a list of breach objects, empty list if clean, None if something went wrong
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}?truncateResponse=false"
    
    try:
        response = requests.get(url, headers=HIBP_HEADERS)
        
        if response.status_code == 200:
            return response.json()  # found breaches, return them
        elif response.status_code == 404:
            return []  # 404 here actually means no breaches found, not an error
        elif response.status_code == 401:
            print("Error: Invalid or missing API key. Check your .env file.")
            return None
        elif response.status_code == 429:
            # hibp rate limits if u hit it too many times, just wait a bit
            print("Error: Rate limited. Please wait a moment and try again.")
            return None
        else:
            print(f"Unexpected error: {response.status_code}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect. Check your internet connection.")
        return None


def check_password(password: str) -> int:
    # this is the cool part - we never actually send the password to any server
    # its called k-anonimity (looked this up, pretty neat concept)
    
    # step 1: hash the password using sha1
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    
    # step 2: only send the first 5 characters of the hash
    prefix = sha1[:5]
    suffix = sha1[5:]  # we keep the rest locally to check against
    
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    
    try:
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"Password API error: {response.status_code}")
            return -1
        
        # api sends back a bunch of hashes that start with our prefix
        # we check locally if our full hash is in there
        hashes = response.text.splitlines()
        for line in hashes:
            returned_suffix, count = line.split(":")
            if returned_suffix == suffix:
                return int(count)  # how many times this password was leaked
        
        return 0  # not found, password is clean
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to password API.")
        return -1