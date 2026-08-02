import whois
import socket
import dns.resolver
import requests

def analyze_domain(domain):

    result = {}

    try:
        w = whois.whois(domain)

        result["domain"] = domain
        result["registrar"] = w.registrar
        result["creation_date"] = str(w.creation_date)
        result["expiration_date"] = str(w.expiration_date)

    except Exception:
        result["domain"] = domain
        result["registrar"] = "Unknown"
        result["creation_date"] = "Unknown"
        result["expiration_date"] = "Unknown"

    try:
        result["ip"] = socket.gethostbyname(domain)
    except Exception:
        result["ip"] = "Unknown"

    try:
        r = requests.get(f"https://{domain}", timeout=5)
        result["https"] = "Yes"
        result["status"] = r.status_code
    except Exception:
        result["https"] = "No"
        result["status"] = "Unavailable"

    try:
        mx = dns.resolver.resolve(domain, "MX")
        result["mx"] = [str(x.exchange) for x in mx]
    except Exception:
        result["mx"] = []

    try:
        ns = dns.resolver.resolve(domain, "NS")
        result["ns"] = [str(x.target) for x in ns]
    except Exception:
        result["ns"] = []

    return result