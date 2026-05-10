import hashlib
import requests
from xposedornot import XposedOrNot

# xposedornot client - no api key needed, its completely free
xon = XposedOrNot()

def check_email(email: str) -> list:
    # checks if the email appeared in any known breaches
    # using xposedornot which is free and doesnt need an api key
    try:
        result = xon.check_email(email)
        
        if not result.breaches:
            return []  # clean, no breaches found
        
        # format it to match what the rest of our code expects
        # each breach becomes a dict with a Name field
        formatted = []
        for breach_name in result.breaches:
            formatted.append({
                "Name": breach_name,
                "BreachDate": "unknown",  # free api doesnt return dates
                "DataClasses": []  # free api doesnt return data types either
            })
        
        return formatted

    except Exception as e:
        print(f"Error checking email: {e}")
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