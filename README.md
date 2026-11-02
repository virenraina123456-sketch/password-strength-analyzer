# Password Strength Analyzer

A Python project that estimates how strong a password is, explains why, and
suggests improvements. Standard library only; works from the command line or a
simple desktop GUI.

## Features
- Entropy estimate based on length and character pool
- Detection of common passwords, dictionary words (including leetspeak such as `P@ssw0rd`),
  sequences (`abcd`, `1234`), keyboard patterns (`qwerty`), repeats and years
- Five strength levels: Very weak, Weak, Fair, Strong, Very strong
- Estimated offline crack time
- Actionable feedback
- Secure password and passphrase generator (`secrets` module)
- Optional breach check with Have I Been Pwned (k-anonymity: only the first 5
  characters of the SHA-1 hash leave your machine)

## Project structure
```
password_strength_analyzer/
├── main.py                  # command-line interface
├── gui.py                   # Tkinter GUI with live feedback
├── analyzer/
│   ├── core.py              # pattern detection, entropy, scoring
│   ├── generator.py         # password / passphrase generator
│   ├── breach.py            # optional HIBP check
│   └── data/common_passwords.txt
├── tests/test_analyzer.py   # unit tests
└── requirements.txt
```

## Usage
```bash
python main.py                      # prompts for password (hidden input)
python main.py "MyP@ssw0rd2024"     # analyze directly (visible in shell history)
python main.py "secret" --json      # JSON output
python main.py "secret" --breach-check
python main.py --generate           # generate a password and passphrase
python gui.py                       # launch the GUI
python -m unittest discover tests   # run tests
```

## How it works
1. **Pool size**: sum of character classes used (26 lower, 26 upper, 10 digits, 33 symbols).
2. **Pattern matching**: finds dictionary words, sequences, keyboard runs, repeats and years,
   then picks the non-overlapping set that explains the password most cheaply.
3. **Entropy**: unmatched characters cost `log2(pool)` bits each; each matched pattern costs
   only the bits an attacker would need to guess it (e.g. a common word costs
   about `log2(rank)` bits).
4. **Score**: Very weak < 28 bits, Weak 28-39, Fair 40-59, Strong 60-79, Very strong 80+.
5. **Crack time**: `2^(bits-1) / 10^10` seconds, assuming a fast offline attack.

## Limitations
- The built-in word list is small (about 120 entries). Replace
  `analyzer/data/common_passwords.txt` with a larger list (e.g. RockYou top 100k, ordered by
  popularity) for better accuracy.
- Entropy is an estimate, not a guarantee. Real attackers use smarter models.
- Never reuse a password because it scored well; use a password manager and MFA.

## Future scope
Larger wordlists, Markov/ML-based guess models, a web front end, a browser extension,
and policy checks (e.g. NIST SP 800-63B).
