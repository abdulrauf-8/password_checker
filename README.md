# 🔐 Password Strength Checker

**DecodeLabs · Cyber Security Project 1 · Batch 2026**

A defensive security tool that evaluates password strength in real time using string analysis, entropy calculation, and breach detection. Built as part of the DecodeLabs Industrial Training Kit.

---

## 📸 Preview

| Python CLI | Browser UI |
|---|---|
| Terminal-based, color-coded output | Live strength meter, check indicators |

---

## 📁 Project Structure

```
password-strength-checker/
├── password_checker.py        # Core logic + CLI interface (Python)
├── password_checker.html      # Standalone browser UI (HTML + JS)
└── README.md
```

---

## ⚙️ Features

- ✅ Real-time password strength rating: **Weak / Medium / Strong / Very Strong**
- ✅ Checks for length, uppercase, digits, and symbols
- ✅ Bonus score for 12+ character passwords
- ✅ Leaked password detection against known breach list
- ✅ Entropy estimate in bits + character pool size
- ✅ Actionable feedback — one tip at a time
- ✅ Timing-safe comparison using `hmac.compare_digest()` (Python version)
- ✅ Eye toggle to show/hide password (HTML version)

---

## 🚀 Getting Started

### Python CLI

**Requirements:** Python 3.6+, no external packages needed.

```bash
python3 password_checker.py
```

Enter any password at the prompt. Type `quit` to exit.

**Example output:**

```
==================================================
🔐 PASSWORD STRENGTH REPORT
==================================================
  Password : *********
  Length   : 9 characters
  Score    : 4 / 5
  Strength : STRONG
--------------------------------------------------
  Check Results:
    ✅  Not Leaked
    ✅  Length 8+
    ❌  Length 12+
    ✅  Has Upper
    ✅  Has Digit
    ✅  Has Symbol
--------------------------------------------------
  Feedback:
    ✅ Excellent! This password meets all security requirements.
==================================================
```

### Browser UI

No server required. Just open the file:

```bash
# Double-click the file, or:
open password_checker.html       # macOS
xdg-open password_checker.html  # Linux
start password_checker.html      # Windows
```

---

## 🧠 How It Works

### Scoring System (0–5)

| Check | Points |
|---|---|
| Length ≥ 8 characters | +1 |
| Length ≥ 12 characters | +1 (bonus) |
| Contains uppercase [A-Z] | +1 |
| Contains digit [0-9] | +1 |
| Contains symbol [!@#$...] | +1 |

| Score | Rating |
|---|---|
| 0–2 | Weak |
| 3 | Medium |
| 4 | Strong |
| 5 | Very Strong |

Leaked passwords are hard-capped at score 1, regardless of complexity.

### Entropy Formula

```
entropy (bits) = length × log₂(pool_size)
```

Where `pool_size` = sum of active character sets (lowercase 26 + uppercase 26 + digits 10 + symbols 32).

### Security Notes

- The Python version uses `hmac.compare_digest()` for constant-time comparison against the leaked password list, preventing timing attacks.
- Python strings are immutable — sensitive data may linger in heap memory until garbage collection. For production use, consider `bytearray` for mutable, wipeable buffers.
- This tool runs 100% client-side / locally. No password is ever sent over a network.

---

## 📚 Concepts Covered

| Concept | Where Applied |
|---|---|
| String handling & conditionals | Core strength logic |
| Data validation | Length gate, pattern checks |
| Entropy & character sets | Pool size + bits calculation |
| Timing attack prevention | `hmac.compare_digest()` |
| Breach list detection | HIBP-style blocklist |
| Pythonic `any()` | Character checks (no verbose loops) |

---

## 🛡️ Part of DecodeLabs Security Track

> Project 1 → Password Strength Checker *(this repo)*
> Project 2 → Hashing & Encryption *(coming next)*

---

## 📄 License

Built for educational purposes as part of the DecodeLabs Industrial Training Program.
