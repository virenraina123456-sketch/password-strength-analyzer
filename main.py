#!/usr/bin/env python3
"""Command-line interface for the Password Strength Analyzer."""
import argparse
import getpass
import json
import sys

from analyzer import analyze, generate_password, generate_passphrase

COLORS = ["\033[91m", "\033[91m", "\033[93m", "\033[92m", "\033[92m"]
RESET = "\033[0m"


def show(res, use_color=True):
    c = COLORS[res.score] if use_color else ""
    r = RESET if use_color else ""
    bar = "#" * (res.score + 1) + "-" * (4 - res.score)
    print(f"\nStrength : {c}{res.level}{r}  [{bar}]")
    print(f"Length   : {res.length}   Character pool: {res.pool_size}")
    print(f"Entropy  : {res.entropy_bits} bits")
    print(f"Crack time (offline, 10 billion guesses/s): {res.crack_time}")
    if res.matches:
        print("Patterns : " + ", ".join(f"{m['kind']} ({m['token']})" for m in res.matches))
    print("\nSuggestions:")
    for tip in res.feedback:
        print(f"  - {tip}")


def main():
    p = argparse.ArgumentParser(description="Analyze password strength.")
    p.add_argument("password", nargs="?", help="password (omit to be prompted securely)")
    p.add_argument("--json", action="store_true", help="output JSON")
    p.add_argument("--breach-check", action="store_true", help="check Have I Been Pwned (needs internet)")
    p.add_argument("--generate", action="store_true", help="generate a strong password and passphrase")
    a = p.parse_args()

    if a.generate:
        print("Password  :", generate_password())
        print("Passphrase:", generate_passphrase())
        return

    pw = a.password if a.password is not None else getpass.getpass("Password: ")
    res = analyze(pw)
    if a.json:
        print(json.dumps(res.to_dict(), indent=2))
    else:
        show(res, sys.stdout.isatty())
    if a.breach_check:
        from analyzer.breach import pwned_count
        try:
            n = pwned_count(pw)
            print(f"\nBreach check: found in {n:,} breaches!" if n else "\nBreach check: not found in known breaches.")
        except Exception as e:
            print(f"\nBreach check failed: {e}")


if __name__ == "__main__":
    main()
