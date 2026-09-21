#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  BLACK HAT HACKERS FORCE
  TAG     : BHHF
  Tool    : BHHF Multi Tool
  Author  : MR MARCO
  Team    : BLACK HAT HACKERS FORCE
  Version : 1.0
  Modules : Password Strength, IP Info, SSL Checker,
            Header Analyzer, URL Scanner, QR Generator,
            Weather Tool
============================================================
"""

import os
import sys
import ssl
import socket
import json
import urllib.request
import urllib.parse
from datetime import datetime

# ---------- QR ছাড়া বাকি সব pure Python ----------
# QR এর জন্য qrcode লাগবে (pip install qrcode[pil])
try:
    import qrcode
    QR_OK = True
except ImportError:
    QR_OK = False


# ---------- Colors ----------
class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    WHITE = "\033[97m"


# ---------- Banner ----------
def banner():
    os.system("clear" if os.name != "nt" else "cls")
    print(f"""{C.RED}{C.BOLD}
    ██████╗ ██╗  ██╗██╗  ██╗███████╗
    ██╔══██╗██║  ██║██║  ██║██╔════╝
    ██████╔╝███████║███████║█████╗
    ██╔══██╗██╔══██║██╔══██║██╔══╝
    ██████╔╝██║  ██║██║  ██║██║
    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝
{C.RESET}{C.WHITE}{C.BOLD}   BLACK HAT HACKERS FORCE{C.RESET}
{C.YELLOW}   ──────────────────────────────────────{C.RESET}
{C.MAGENTA}      TAG     : {C.BOLD}BHHF{C.RESET}
{C.GREEN}      Tool    : {C.BOLD}BHHF Multi Tool{C.RESET}
{C.GREEN}      Author  : {C.BOLD}MR MARCO{C.RESET}
{C.GREEN}      Team    : {C.BOLD}BLACK HAT HACKERS FORCE{C.RESET}
{C.GREEN}      Version : {C.BOLD}1.0{C.RESET}
{C.YELLOW}   ──────────────────────────────────────{C.RESET}
""")


# ---------- Menu ----------
def menu():
    print(f"""{C.CYAN}{C.BOLD}  ┌──────────────── MAIN MENU ────────────────┐{C.RESET}
{C.WHITE}  │                                            │
  │  {C.GREEN}[1]{C.WHITE}  Password Strength Checker              │
  │  {C.GREEN}[2]{C.WHITE}  IP Address Info                        │
  │  {C.GREEN}[3]{C.WHITE}  SSL Certificate Checker                │
  │  {C.GREEN}[4]{C.WHITE}  HTTP Header Analyzer                   │
  │  {C.GREEN}[5]{C.WHITE}  URL / Phishing Scanner                 │
  │  {C.GREEN}[6]{C.WHITE}  QR Code Generator                      │
  │  {C.GREEN}[7]{C.WHITE}  Weather Info (API)                     │
  │                                            │
  │  {C.RED}[0]{C.WHITE}  Exit                                   │
  │                                            │
  └────────────────────────────────────────────┘{C.RESET}
""")


# ============================================================
# MODULE 1 : PASSWORD STRENGTH CHECKER
# ============================================================
def password_strength():
    print(f"\n{C.YELLOW}═══ PASSWORD STRENGTH CHECKER ═══{C.RESET}\n")
    pw = input(f"{C.CYAN}[?]{C.RESET} Enter password to check: ")

    score = 0
    tips = []

    if len(pw) >= 8:
        score += 1
    else:
        tips.append("Use at least 8 characters")

    if len(pw) >= 12:
        score += 1
    if len(pw) >= 16:
        score += 1
    else:
        tips.append("Use 16+ characters for better strength")

    if any(c.isupper() for c in pw):
        score += 1
    else:
        tips.append("Add UPPERCASE letters")

    if any(c.islower() for c in pw):
        score += 1
    else:
        tips.append("Add lowercase letters")

    if any(c.isdigit() for c in pw):
        score += 1
    else:
        tips.append("Add numbers")

    if any(not c.isalnum() for c in pw):
        score += 1
    else:
        tips.append("Add special symbols (!@#$%)")

    # common patterns
    common = ["123456", "password", "qwerty", "admin", "111111", "abc123"]
    if any(c in pw.lower() for c in common):
        score -= 2
        tips.append("Avoid common words like 'password', '123456'")

    print()
    if score <= 2:
        label = f"{C.RED}Weak{C.RESET}"
    elif score <= 4:
        label = f"{C.YELLOW}Medium{C.RESET}"
    elif score <= 6:
        label = f"{C.GREEN}Strong{C.RESET}"
    else:
        label = f"{C.GREEN}{C.BOLD}Very Strong{C.RESET}"

    print(f"  {C.CYAN}Length     :{C.RESET} {len(pw)}")
    print(f"  {C.CYAN}Score      :{C.RESET} {score}/7")
    print(f"  {C.CYAN}Strength   :{C.RESET} {label}")

    if tips:
        print(f"\n  {C.YELLOW}Suggestions:{C.RESET}")
        for t in tips:
            print(f"    - {t}")
    print()


# ============================================================
# MODULE 2 : IP ADDRESS INFO
# ============================================================
def ip_info():
    print(f"\n{C.YELLOW}═══ IP ADDRESS INFO ═══{C.RESET}\n")
    ip = input(f"{C.CYAN}[?]{C.RESET} Enter IP (blank = your IP): ").strip()

    url = f"http://ip-api.com/json/{ip}" if ip else "http://ip-api.com/json/"

    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.loads(r.read().decode())

        if data.get("status") != "success":
            print(f"{C.RED}[!]{C.RESET} Could not fetch info: {data.get('message','unknown')}")
            return

        print()
        print(f"  {C.CYAN}IP         :{C.RESET} {data.get('query','-')}")
        print(f"  {C.CYAN}Country    :{C.RESET} {data.get('country','-')} ({data.get('countryCode','-')})")
        print(f"  {C.CYAN}Region     :{C.RESET} {data.get('regionName','-')}")
        print(f"  {C.CYAN}City       :{C.RESET} {data.get('city','-')}")
        print(f"  {C.CYAN}ZIP        :{C.RESET} {data.get('zip','-')}")
        print(f"  {C.CYAN}Latitude   :{C.RESET} {data.get('lat','-')}")
        print(f"  {C.CYAN}Longitude  :{C.RESET} {data.get('lon','-')}")
        print(f"  {C.CYAN}Timezone   :{C.RESET} {data.get('timezone','-')}")
        print(f"  {C.CYAN}ISP        :{C.RESET} {data.get('isp','-')}")
        print(f"  {C.CYAN}Org        :{C.RESET} {data.get('org','-')}")
        print(f"  {C.CYAN}AS         :{C.RESET} {data.get('as','-')}")
        print()

    except Exception as e:
        print(f"{C.RED}[!]{C.RESET} Error: {e}")


# ============================================================
# MODULE 3 : SSL CERTIFICATE CHECKER
# ============================================================
def ssl_checker():
    print(f"\n{C.YELLOW}═══ SSL CERTIFICATE CHECKER ═══{C.RESET}\n")
    host = input(f"{C.CYAN}[?]{C.RESET} Enter domain (e.g. google.com): ").strip()
    if not host:
        print(f"{C.RED}[!]{C.RESET} Domain required.")
        return

    host = host.replace("https://", "").replace("http://", "").split("/")[0]
    port = 443

    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=10) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()

        subject = dict(x[0] for x in cert['subject'])
        issuer = dict(x[0] for x in cert['issuer'])

        valid_from = cert['notBefore']
        valid_until = cert['notAfter']

        exp = datetime.strptime(valid_until, "%b %d %H:%M:%S %Y %Z")
        days_left = (exp - datetime.utcnow()).days

        print()
        print(f"  {C.CYAN}Domain       :{C.RESET} {host}")
        print(f"  {C.CYAN}Common Name  :{C.RESET} {subject.get('commonName','-')}")
        print(f"  {C.CYAN}Issued To    :{C.RESET} {subject.get('organizationName','-')}")
        print(f"  {C.CYAN}Issuer       :{C.RESET} {issuer.get('organizationName','-')}")
        print(f"  {C.CYAN}Valid From   :{C.RESET} {valid_from}")
        print(f"  {C.CYAN}Valid Until  :{C.RESET} {valid_until}")

        if days_left < 0:
            print(f"  {C.RED}Status       : EXPIRED{C.RESET}")
        elif days_left < 15:
            print(f"  {C.YELLOW}Status       : Expiring soon ({days_left} days){C.RESET}")
        else:
            print(f"  {C.GREEN}Status       : Valid ({days_left} days left){C.RESET}")
        print()

    except Exception as e:
        print(f"{C.RED}[!]{C.RESET} Error: {e}")


# ============================================================
# MODULE 4 : HTTP HEADER ANALYZER
# ============================================================
def header_analyzer():
    print(f"\n{C.YELLOW}═══ HTTP HEADER ANALYZER ═══{C.RESET}\n")
    url = input(f"{C.CYAN}[?]{C.RESET} Enter URL (e.g. https://example.com): ").strip()
    if not url:
        print(f"{C.RED}[!]{C.RESET} URL required.")
        return
    if not url.startswith("http"):
        url = "https://" + url

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            headers = dict(r.headers)

        print()
        for k, v in headers.items():
            print(f"  {C.CYAN}{k}:{C.RESET} {v}")

        print(f"\n  {C.YELLOW}── Security Header Check ──{C.RESET}")
        sec = {
            "Strict-Transport-Security": "HSTS missing - not forcing HTTPS",
            "Content-Security-Policy": "CSP missing - XSS risk",
            "X-Frame-Options": "Clickjacking risk",
            "X-Content-Type-Options": "MIME sniffing risk",
            "Referrer-Policy": "Referrer leak risk",
        }
        for h, msg in sec.items():
            if h in headers:
                print(f"    {C.GREEN}[OK]{C.RESET} {h}")
            else:
                print(f"    {C.RED}[MISSING]{C.RESET} {h} - {msg}")
        print()

    except Exception as e:
        print(f"{C.RED}[!]{C.RESET} Error: {e}")


# ============================================================
# MODULE 5 : URL / PHISHING SCANNER
# ============================================================
def url_scanner():
    print(f"\n{C.YELLOW}═══ URL / PHISHING SCANNER ═══{C.RESET}\n")
    url = input(f"{C.CYAN}[?]{C.RESET} Enter URL to scan: ").strip()
    if not url:
        print(f"{C.RED}[!]{C.RESET} URL required.")
        return

    score = 0
    flags = []

    lower = url.lower()

    if not lower.startswith("https://"):
        score += 2
        flags.append("Not using HTTPS")

    if "@" in url:
        score += 3
        flags.append("Contains '@' - classic phishing trick")

    if len(url) > 75:
        score += 1
        flags.append("Very long URL")

    if url.count("-") > 3:
        score += 1
        flags.append("Too many hyphens")

    if any(x in lower for x in ["login", "verify", "update", "secure", "account", "signin"]):
        score += 1
        flags.append("Contains sensitive keywords")

    # IP-based URL
    import re
    if re.match(r"^https?://\d+\.\d+\.\d+\.\d+", lower):
        score += 3
        flags.append("Uses raw IP instead of domain")

    # suspicious TLDs
    sus_tlds = [".tk", ".ml", ".ga", ".cf", ".gq", ".xyz", ".top", ".click"]
    for t in sus_tlds:
        if lower.endswith(t) or f"{t}/" in lower:
            score += 2
            flags.append(f"Suspicious TLD: {t}")

    # brand in subdomain
    brands = ["facebook", "google", "paypal", "binance", "bkash", "nagad", "railway"]
    for b in brands:
        if b in lower and not lower.split("//")[-1].startswith(b):
            score += 2
            flags.append(f"Possible brand spoofing: {b}")

    print()
    print(f"  {C.CYAN}URL    :{C.RESET} {url}")
    print(f"  {C.CYAN}Score  :{C.RESET} {score}")

    if score == 0:
        print(f"  {C.GREEN}Result : Looks SAFE (no red flags){C.RESET}")
    elif score <= 3:
        print(f"  {C.YELLOW}Result : SUSPICIOUS - be careful{C.RESET}")
    else:
        print(f"  {C.RED}Result : LIKELY PHISHING - do NOT open{C.RESET}")

    if flags:
        print(f"\n  {C.YELLOW}Flags:{C.RESET}")
        for f in flags:
            print(f"    - {f}")
    print()


# ============================================================
# MODULE 6 : QR CODE GENERATOR
# ============================================================
def qr_generator():
    print(f"\n{C.YELLOW}═══ QR CODE GENERATOR ═══{C.RESET}\n")

    if not QR_OK:
        print(f"{C.RED}[!]{C.RESET} 'qrcode' module not installed.")
        print(f"    Run: {C.CYAN}pip install qrcode[pil]{C.RESET}")
        return

    data = input(f"{C.CYAN}[?]{C.RESET} Enter text or URL: ").strip()
    if not data:
        print(f"{C.RED}[!]{C.RESET} Data required.")
        return

    filename = input(f"{C.CYAN}[?]{C.RESET} Save as (default qr.png): ").strip() or "qr.png"
    if not filename.endswith(".png"):
        filename += ".png"

    try:
        img = qrcode.make(data)
        img.save(filename)
        print(f"{C.GREEN}[OK]{C.RESET} QR saved: {filename}")
    except Exception as e:
        print(f"{C.RED}[!]{C.RESET} Error: {e}")


# ============================================================
# MODULE 7 : WEATHER INFO
# ============================================================
def weather_info():
    print(f"\n{C.YELLOW}═══ WEATHER INFO ═══{C.RESET}\n")
    print(f"{C.MAGENTA}Get free API key from: https://openweathermap.org/api{C.RESET}\n")

    api_key = input(f"{C.CYAN}[?]{C.RESET} Enter OpenWeather API key: ").strip()
    if not api_key:
        print(f"{C.RED}[!]{C.RESET} API key required.")
        return

    city = input(f"{C.CYAN}[?]{C.RESET} Enter city name: ").strip()
    if not city:
        print(f"{C.RED}[!]{C.RESET} City required.")
        return

    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"q={urllib.parse.quote(city)}&appid={api_key}&units=metric"
    )

    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.loads(r.read().decode())

        if data.get("cod") != 200:
            print(f"{C.RED}[!]{C.RESET} {data.get('message','error')}")
            return

        main = data["main"]
        wind = data["wind"]
        weather = data["weather"][0]

        print()
        print(f"  {C.CYAN}City        :{C.RESET} {data['name']}, {data['sys']['country']}")
        print(f"  {C.CYAN}Condition   :{C.RESET} {weather['main']} - {weather['description']}")
        print(f"  {C.CYAN}Temperature :{C.RESET} {main['temp']}°C (feels like {main['feels_like']}°C)")
        print(f"  {C.CYAN}Min / Max   :{C.RESET} {main['temp_min']}°C / {main['temp_max']}°C")
        print(f"  {C.CYAN}Humidity    :{C.RESET} {main['humidity']}%")
        print(f"  {C.CYAN}Pressure    :{C.RESET} {main['pressure']} hPa")
        print(f"  {C.CYAN}Wind Speed  :{C.RESET} {wind['speed']} m/s")
        print()

    except Exception as e:
        print(f"{C.RED}[!]{C.RESET} Error: {e}")


# ============================================================
# MAIN LOOP
# ============================================================
def main():
    banner()

    actions = {
        "1": ("Password Strength Checker", password_strength),
        "2": ("IP Address Info", ip_info),
        "3": ("SSL Certificate Checker", ssl_checker),
        "4": ("HTTP Header Analyzer", header_analyzer),
        "5": ("URL / Phishing Scanner", url_scanner),
        "6": ("QR Code Generator", qr_generator),
        "7": ("Weather Info", weather_info),
    }

    while True:
        menu()
        choice = input(f"{C.CYAN}[?]{C.RESET} Select option: ").strip()

        if choice == "0":
            print(f"\n{C.MAGENTA}  BHHF | MR MARCO | BLACK HAT HACKERS FORCE{C.RESET}")
            print(f"{C.YELLOW}  Goodbye.{C.RESET}\n")
            sys.exit(0)

        if choice in actions:
            name, func = actions[choice]
            func()
            input(f"\n{C.YELLOW}Press Enter to return to menu...{C.RESET}")
            banner()
        else:
            print(f"{C.RED}[!]{C.RESET} Invalid option. Try 0-7.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C.RED}[!]{C.RESET} Stopped.")
        sys.exit(0)