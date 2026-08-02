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

    except:
        result["registrar"] = "Unknown"
        result["creation_date"] = "Unknown"
        result["expiration_date"] = "Unknown"

    # IP
    try:
        result["ip"] = socket.gethostbyname(domain)
    except:
        result["ip"] = "Unknown"

    # SSL / HTTPS
    try:
        r = requests.get(f"https://{domain}", timeout=5)
        result["https"] = "Yes"
        result["status"] = r.status_code
    except:
        result["https"] = "No"
        result["status"] = "Unavailable"

    # MX
    try:
        mx = dns.resolver.resolve(domain, "MX")
        result["mx"] = [str(x.exchange) for x in mx]
    except:
        result["mx"] = []

    # NS
    try:
        ns = dns.resolver.resolve(domain, "NS")
        result["ns"] = [str(x.target) for x in ns]
    except:
        result["ns"] = []

    return result

with tab_domain:

    if "." in query:

        info = analyze_domain(query)

        st.metric("Domain", info["domain"])
        st.metric("Registrar", info["registrar"])

        st.metric("HTTPS", info["https"])
        st.metric("Status", info["status"])

        st.metric("IP Address", info["ip"])

        st.write("### Created")
        st.write(info["creation_date"])

        st.write("### Expires")
        st.write(info["expiration_date"])

        st.write("### Name Servers")
        st.write(info["ns"])

        st.write("### Mail Servers")
        st.write(info["mx"])

    else:

        st.info("Enter a website such as google.com")