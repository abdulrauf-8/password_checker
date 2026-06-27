"""
DecodeLabs | Cyber Security - Project 1
Password Strength Checker — Styled Python GUI
Batch: 2026
Run: python3 password_checker_gui.py
Requirements: Python 3.6+ (tkinter is built-in, no pip install needed)
"""

import tkinter as tk
from tkinter import ttk
import math
import hmac

# ── Constants ──────────────────────────────────────────────────────────────────

LEAKED = {
    "password", "123456", "password123", "admin", "letmein",
    "welcome", "monkey", "dragon", "master", "123456789",
    "qwerty", "abc123", "iloveyou", "1234567890", "sunshine",
    "princess", "football", "charlie", "donald", "password1"
}

C = {
    "bg"           : "#0f1117",
    "card"         : "#1a1d27",
    "card2"        : "#22263a",
    "border"       : "#2e3348",
    "accent"       : "#6366f1",
    "accent2"      : "#818cf8",
    "text"         : "#f1f5f9",
    "muted"        : "#64748b",
    "weak"         : "#ef4444",
    "medium"       : "#f59e0b",
    "strong"       : "#22c55e",
    "very_strong"  : "#10b981",
    "ok_bg"        : "#052e16",
    "ok_fg"        : "#22c55e",
    "bad_bg"       : "#2d0a0a",
    "bad_fg"       : "#ef4444",
    "off_bg"       : "#1e2235",
    "off_fg"       : "#475569",
    "leaked_bg"    : "#2d0a0a",
    "leaked_fg"    : "#fca5a5",
    "tip_bg"       : "#1c1a07",
    "tip_fg"       : "#fde68a",
    "bar_empty"    : "#1e2235",
    "input_bg"     : "#12151f",
    "input_fg"     : "#f1f5f9",
    "cursor"       : "#6366f1",
    "white"        : "#ffffff",
}

FONT_HEAD  = ("Segoe UI", 20, "bold")
FONT_SUB   = ("Segoe UI", 10)
FONT_LABEL = ("Segoe UI", 11)
FONT_MONO  = ("Consolas", 13)
FONT_SMALL = ("Segoe UI", 9)
FONT_ICON  = ("Segoe UI Emoji", 14)
FONT_BIG   = ("Segoe UI Emoji", 36)

CHECKS = [
    ("length",  "At least 8 characters",       "📏"),
    ("upper",   "Uppercase letter  (A – Z)",   "🔠"),
    ("digit",   "Number  (0 – 9)",             "🔢"),
    ("symbol",  "Symbol  (! @ # $ % …)",       "✳️"),
    ("len12",   "12 + characters  (bonus)",    "⭐"),
]

# ── Logic ──────────────────────────────────────────────────────────────────────

def analyse(pw):
    if not pw:
        return None

    leaked = any(hmac.compare_digest(pw.lower(), k) for k in LEAKED)
    length = len(pw) >= 8
    len12  = len(pw) >= 12
    upper  = any(c.isupper() for c in pw)
    digit  = any(c.isdigit() for c in pw)
    symbol = any(not c.isalnum() for c in pw)

    score = sum([length, len12, upper, digit, symbol])
    if leaked:
        score = min(score, 1)

    pool = 0
    if any(c.islower() for c in pw): pool += 26
    if upper:  pool += 26
    if digit:  pool += 10
    if symbol: pool += 32
    entropy = round(len(pw) * math.log2(pool)) if pool else 0

    tips = []
    if not length: tips.append("Use at least 8 characters.")
    if not upper:  tips.append("Add an uppercase letter.")
    if not digit:  tips.append("Add a number (0–9).")
    if not symbol: tips.append("Add a symbol like !@#$.")
    if length and upper and digit and symbol and not len12:
        tips.append("Try 12+ characters for maximum strength.")

    labels = {0:"—", 1:"Weak", 2:"Weak", 3:"Medium", 4:"Strong", 5:"Very Strong"}
    colors = {
        0: C["muted"], 1: C["weak"], 2: C["weak"],
        3: C["medium"], 4: C["strong"], 5: C["very_strong"]
    }

    return {
        "score"  : score,
        "leaked" : leaked,
        "label"  : "Leaked — change it" if leaked else labels[score],
        "color"  : C["weak"] if leaked else colors[score],
        "checks" : {"length": length, "upper": upper,
                    "digit": digit, "symbol": symbol, "len12": len12},
        "entropy": entropy,
        "pool"   : pool,
        "tip"    : tips[0] if tips and not leaked else "",
        "length" : len(pw),
    }

# ── App ────────────────────────────────────────────────────────────────────────

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Strength Checker")
        self.resizable(False, False)
        self.configure(bg=C["bg"])
        self._show = False
        self._build()
        self._reset()
        # Center window
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"+{x}+{y}")

    # ── Build UI ───────────────────────────────────────────────────────────────

    def _build(self):
        outer = tk.Frame(self, bg=C["bg"])
        outer.pack(padx=28, pady=24)

        # ── Header ─────────────────────────────────────────────────────────
        hdr = tk.Frame(outer, bg=C["bg"])
        hdr.pack(fill="x", pady=(0, 18))

        tk.Label(hdr, text="🔐", font=FONT_BIG,
                 bg=C["bg"], fg=C["white"]).pack(side="left", padx=(0, 12))

        txt = tk.Frame(hdr, bg=C["bg"])
        txt.pack(side="left")
        tk.Label(txt, text="Password Strength Checker",
                 font=FONT_HEAD, bg=C["bg"], fg=C["text"]).pack(anchor="w")
        tk.Label(txt, text="DecodeLabs  ·  Cyber Security Project 1  ·  Batch 2026",
                 font=FONT_SMALL, bg=C["bg"], fg=C["muted"]).pack(anchor="w")

        # ── Card ───────────────────────────────────────────────────────────
        card = tk.Frame(outer, bg=C["card"],
                        highlightbackground=C["border"], highlightthickness=1)
        card.pack(fill="x")

        inner = tk.Frame(card, bg=C["card"])
        inner.pack(padx=22, pady=20, fill="x")

        # Input label
        tk.Label(inner, text="Enter your password",
                 font=FONT_LABEL, bg=C["card"],
                 fg=C["muted"]).pack(anchor="w", pady=(0, 5))

        # Input row
        row = tk.Frame(inner, bg=C["input_bg"],
                       highlightbackground=C["border"], highlightthickness=1)
        row.pack(fill="x")

        self.pw_var = tk.StringVar()
        self.pw_var.trace_add("write", lambda *_: self._update())

        self.entry = tk.Entry(
            row, textvariable=self.pw_var, show="●",
            font=FONT_MONO,
            bg=C["input_bg"], fg=C["input_fg"],
            insertbackground=C["cursor"],
            relief="flat", bd=0,
            highlightthickness=0,
        )
        self.entry.pack(side="left", fill="x", expand=True,
                        ipady=10, ipadx=10)

        self.eye = tk.Button(
            row, text="👁", font=FONT_ICON,
            bg=C["input_bg"], fg=C["muted"],
            relief="flat", bd=0, cursor="hand2",
            activebackground=C["input_bg"], activeforeground=C["accent2"],
            command=self._toggle
        )
        self.eye.pack(side="right", padx=8)

        # ── Strength meter ─────────────────────────────────────────────────
        meter_frame = tk.Frame(inner, bg=C["card"])
        meter_frame.pack(fill="x", pady=(14, 0))

        bars_row = tk.Frame(meter_frame, bg=C["card"])
        bars_row.pack(fill="x")
        self.bars = []
        for i in range(5):
            b = tk.Frame(bars_row, bg=C["bar_empty"], height=7)
            b.pack(side="left", expand=True, fill="x",
                   padx=(0 if i == 0 else 4, 0))
            b.pack_propagate(False)
            self.bars.append(b)

        lrow = tk.Frame(meter_frame, bg=C["card"])
        lrow.pack(fill="x", pady=(6, 0))
        self.str_lbl = tk.Label(lrow, text="",
                                font=("Segoe UI", 12, "bold"),
                                bg=C["card"], fg=C["muted"])
        self.str_lbl.pack(side="left")
        self.score_lbl = tk.Label(lrow, text="",
                                  font=FONT_SMALL,
                                  bg=C["card"], fg=C["muted"])
        self.score_lbl.pack(side="right")

        # ── Leaked banner ──────────────────────────────────────────────────
        self.leaked_frame = tk.Frame(inner, bg=C["leaked_bg"],
                                     highlightbackground=C["weak"],
                                     highlightthickness=1)
        tk.Label(self.leaked_frame,
                 text="⚠️  This password appears in known breach lists. Don't use it.",
                 font=FONT_LABEL, bg=C["leaked_bg"], fg=C["leaked_fg"],
                 wraplength=380, justify="left").pack(padx=12, pady=8)

        # ── Divider ────────────────────────────────────────────────────────
        tk.Frame(inner, bg=C["border"], height=1).pack(fill="x", pady=14)

        # ── Check rows ─────────────────────────────────────────────────────
        checks_frame = tk.Frame(inner, bg=C["card"])
        checks_frame.pack(fill="x")
        self.chk = {}
        for key, label, icon in CHECKS:
            fr = tk.Frame(checks_frame, bg=C["card"])
            fr.pack(fill="x", pady=4)

            dot = tk.Label(fr, text="–", width=3,
                           font=("Segoe UI", 10, "bold"),
                           fg=C["off_fg"], bg=C["off_bg"],
                           relief="flat")
            dot.pack(side="left", ipadx=2, ipady=2)

            tk.Label(fr, text=icon, font=FONT_ICON,
                     bg=C["card"], fg=C["muted"]).pack(side="left", padx=(8, 4))

            lbl = tk.Label(fr, text=label, font=FONT_LABEL,
                           bg=C["card"], fg=C["off_fg"])
            lbl.pack(side="left")

            self.chk[key] = (dot, lbl)

        # ── Tip box ────────────────────────────────────────────────────────
        self.tip_frame = tk.Frame(inner, bg=C["tip_bg"],
                                  highlightbackground="#78350f",
                                  highlightthickness=1)
        self.tip_lbl = tk.Label(self.tip_frame, text="",
                                font=FONT_LABEL, bg=C["tip_bg"],
                                fg=C["tip_fg"], wraplength=380, justify="left")
        self.tip_lbl.pack(padx=12, pady=8)

        # ── Divider ────────────────────────────────────────────────────────
        tk.Frame(inner, bg=C["border"], height=1).pack(fill="x", pady=14)

        # ── Stats ──────────────────────────────────────────────────────────
        stats = tk.Frame(inner, bg=C["card2"],
                         highlightbackground=C["border"], highlightthickness=1)
        stats.pack(fill="x")

        stats_inner = tk.Frame(stats, bg=C["card2"])
        stats_inner.pack(padx=14, pady=10, fill="x")

        def stat(parent, label, attr):
            r = tk.Frame(parent, bg=C["card2"])
            r.pack(fill="x", pady=3)
            tk.Label(r, text=label, font=FONT_SMALL,
                     bg=C["card2"], fg=C["muted"]).pack(side="left")
            v = tk.Label(r, text="—", font=("Consolas", 10, "bold"),
                         bg=C["card2"], fg=C["text"])
            v.pack(side="right")
            setattr(self, attr, v)

        stat(stats_inner, "Password length",  "stat_len")
        stat(stats_inner, "Character pool",   "stat_pool")
        stat(stats_inner, "Entropy estimate", "stat_ent")

        # ── Footer ─────────────────────────────────────────────────────────
        tk.Label(outer,
                 text="🛡  100% offline — your password never leaves this device",
                 font=FONT_SMALL, bg=C["bg"], fg=C["muted"]).pack(pady=(12, 0))

        self.entry.focus()

    # ── Interactions ───────────────────────────────────────────────────────────

    def _toggle(self):
        self._show = not self._show
        self.entry.config(show="" if self._show else "●")
        self.eye.config(text="🔒" if self._show else "👁")

    def _reset(self):
        for b in self.bars:
            b.config(bg=C["bar_empty"])
        self.str_lbl.config(text="Type a password above", fg=C["muted"])
        self.score_lbl.config(text="")
        self.leaked_frame.pack_forget()
        self.tip_frame.pack_forget()
        for key, _ , __ in CHECKS:
            dot, lbl = self.chk[key]
            dot.config(text="–", fg=C["off_fg"], bg=C["off_bg"])
            lbl.config(fg=C["off_fg"])
        self.stat_len.config(text="—")
        self.stat_pool.config(text="—")
        self.stat_ent.config(text="—")

    def _update(self):
        pw = self.pw_var.get()
        if not pw:
            self._reset()
            return

        r = analyse(pw)

        # Bars
        score = r["score"]
        color = r["color"]
        for i, b in enumerate(self.bars):
            b.config(bg=color if i < score else C["bar_empty"])

        # Labels
        self.str_lbl.config(text=r["label"], fg=color)
        self.score_lbl.config(text=f"{score} / 5")

        # Leaked
        if r["leaked"]:
            self.leaked_frame.pack(fill="x", pady=(10, 0))
        else:
            self.leaked_frame.pack_forget()

        # Checks
        for key, _, __ in CHECKS:
            dot, lbl = self.chk[key]
            passed = r["checks"][key]
            if passed:
                dot.config(text="✓", fg=C["ok_fg"], bg=C["ok_bg"])
                lbl.config(fg=C["text"])
            else:
                dot.config(text="✗", fg=C["bad_fg"], bg=C["bad_bg"])
                lbl.config(fg=C["muted"])

        # Tip
        if r["tip"]:
            self.tip_lbl.config(text="💡  " + r["tip"])
            self.tip_frame.pack(fill="x", pady=(10, 0))
        else:
            self.tip_frame.pack_forget()

        # Stats
        self.stat_len.config(text=f"{r['length']} chars")
        self.stat_pool.config(text=f"{r['pool']} chars")
        self.stat_ent.config(text=f"{r['entropy']} bits")


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = App()
    app.mainloop()
