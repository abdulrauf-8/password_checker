"""
DecodeLabs | Cyber Security - Project 1
Password Strength Checker — Python GUI (tkinter)
Batch: 2026
Run: python3 password_checker_gui.py
"""

import tkinter as tk
from tkinter import font as tkfont
import math

# ── Data ──────────────────────────────────────────────────────────────────────

LEAKED = {
    "password", "123456", "password123", "admin", "letmein",
    "welcome", "monkey", "dragon", "master", "123456789",
    "qwerty", "abc123", "iloveyou", "1234567890", "sunshine",
    "princess", "football", "charlie", "donald", "password1"
}

COLORS = {
    "bg":        "#f0f2f5",
    "card":      "#ffffff",
    "border":    "#e2e5ea",
    "text":      "#111111",
    "muted":     "#888888",
    "weak":      "#ef4444",
    "medium":    "#f59e0b",
    "strong":    "#22c55e",
    "bar_empty": "#e5e7eb",
    "check_ok_bg":   "#dcfce7",
    "check_ok_fg":   "#16a34a",
    "check_bad_bg":  "#fee2e2",
    "check_bad_fg":  "#dc2626",
    "check_off_bg":  "#e5e7eb",
    "check_off_fg":  "#aaaaaa",
    "leaked_bg": "#fee2e2",
    "leaked_fg": "#991b1b",
    "tip_bg":    "#fefce8",
    "tip_fg":    "#854d0e",
    "input_bg":  "#f9fafb",
    "accent":    "#3b82f6",
}

CHECKS = [
    ("length",  "At least 8 characters"),
    ("upper",   "Uppercase letter (A–Z)"),
    ("digit",   "Number (0–9)"),
    ("symbol",  "Symbol  (!@#$%^&*...)"),
    ("len12",   "12+ characters  (bonus)"),
]

# ── Logic ─────────────────────────────────────────────────────────────────────

def analyse(pw):
    if not pw:
        return None

    leaked  = pw.lower() in LEAKED
    length  = len(pw) >= 8
    len12   = len(pw) >= 12
    upper   = any(c.isupper() for c in pw)
    digit   = any(c.isdigit() for c in pw)
    symbol  = any(not c.isalnum() for c in pw)

    score = sum([length, len12, upper, digit, symbol])
    if leaked:
        score = min(score, 1)

    pool = 0
    if any(c.islower() for c in pw): pool += 26
    if upper:                         pool += 26
    if digit:                         pool += 10
    if symbol:                        pool += 32
    entropy = round(len(pw) * math.log2(pool)) if pool else 0

    tips = []
    if not length: tips.append("Use at least 8 characters.")
    if not upper:  tips.append("Add an uppercase letter.")
    if not digit:  tips.append("Add a number (0–9).")
    if not symbol: tips.append("Add a symbol like !@#$.")
    if length and upper and digit and symbol and not len12:
        tips.append("Try 12+ characters for maximum strength.")

    return {
        "score":   score,
        "leaked":  leaked,
        "checks":  {"length": length, "upper": upper,
                    "digit": digit, "symbol": symbol, "len12": len12},
        "entropy": entropy,
        "pool":    pool,
        "tip":     tips[0] if tips and not leaked else "",
    }

# ── App ───────────────────────────────────────────────────────────────────────

class PasswordApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Strength Checker — DecodeLabs Project 1")
        self.resizable(False, False)
        self.configure(bg=COLORS["bg"])

        self._show_pw = False
        self._build_ui()
        self._reset()

    # ── UI construction ───────────────────────────────────────────────────────

    def _build_ui(self):
        card = tk.Frame(self, bg=COLORS["card"],
                        highlightbackground=COLORS["border"],
                        highlightthickness=1)
        card.pack(padx=28, pady=28, fill="both")

        pad = {"padx": 24, "pady": 0}

        # Header
        hdr = tk.Frame(card, bg=COLORS["card"])
        hdr.pack(fill="x", **pad, pady=(22, 4))
        tk.Label(hdr, text="🔐", font=("Segoe UI Emoji", 22),
                 bg=COLORS["card"]).pack(side="left")
        info = tk.Frame(hdr, bg=COLORS["card"])
        info.pack(side="left", padx=8)
        tk.Label(info, text="Password Strength Checker",
                 font=("Segoe UI", 13, "bold"),
                 fg=COLORS["text"], bg=COLORS["card"]).pack(anchor="w")
        tk.Label(info, text="DecodeLabs · Cyber Security Project 1 · Batch 2026",
                 font=("Segoe UI", 9), fg=COLORS["muted"],
                 bg=COLORS["card"]).pack(anchor="w")

        self._sep(card)

        # Input label
        tk.Label(card, text="Enter your password",
                 font=("Segoe UI", 10), fg=COLORS["muted"],
                 bg=COLORS["card"]).pack(anchor="w", **pad, pady=(6, 3))

        # Input row
        row = tk.Frame(card, bg=COLORS["card"])
        row.pack(fill="x", **pad, pady=(0, 4))

        self.pw_var = tk.StringVar()
        self.pw_var.trace_add("write", lambda *_: self._on_change())

        self.entry = tk.Entry(row, textvariable=self.pw_var, show="•",
                              font=("Courier New", 14),
                              bg=COLORS["input_bg"], fg=COLORS["text"],
                              insertbackground=COLORS["text"],
                              relief="flat", bd=0,
                              highlightbackground=COLORS["border"],
                              highlightcolor=COLORS["accent"],
                              highlightthickness=1)
        self.entry.pack(side="left", fill="x", expand=True,
                        ipady=8, ipadx=6)

        self.eye_btn = tk.Button(row, text="👁", font=("Segoe UI Emoji", 13),
                                 bg=COLORS["card"], fg=COLORS["muted"],
                                 relief="flat", cursor="hand2", bd=0,
                                 activebackground=COLORS["card"],
                                 command=self._toggle_pw)
        self.eye_btn.pack(side="left", padx=(6, 0))

        # Strength bars
        bars_frame = tk.Frame(card, bg=COLORS["card"])
        bars_frame.pack(fill="x", **pad, pady=(8, 2))
        self.bars = []
        for _ in range(5):
            b = tk.Frame(bars_frame, bg=COLORS["bar_empty"],
                         height=6, width=60)
            b.pack(side="left", expand=True, fill="x",
                   padx=3, pady=0)
            b.pack_propagate(False)
            self.bars.append(b)

        # Strength label row
        lrow = tk.Frame(card, bg=COLORS["card"])
        lrow.pack(fill="x", **pad, pady=(2, 8))
        self.strength_lbl = tk.Label(lrow, text="—",
                                     font=("Segoe UI", 11, "bold"),
                                     fg=COLORS["muted"], bg=COLORS["card"])
        self.strength_lbl.pack(side="left")
        self.score_lbl = tk.Label(lrow, text="",
                                  font=("Segoe UI", 10),
                                  fg=COLORS["muted"], bg=COLORS["card"])
        self.score_lbl.pack(side="right")

        # Leaked warning
        self.leaked_frame = tk.Frame(card, bg=COLORS["leaked_bg"],
                                     highlightbackground="#fca5a5",
                                     highlightthickness=1)
        self.leaked_lbl = tk.Label(self.leaked_frame,
                                   text="⚠  This password appears in known breach lists. Don't use it.",
                                   font=("Segoe UI", 10),
                                   fg=COLORS["leaked_fg"],
                                   bg=COLORS["leaked_bg"],
                                   wraplength=360, justify="left")
        self.leaked_lbl.pack(padx=10, pady=7)

        self._sep(card)

        # Check rows
        checks_frame = tk.Frame(card, bg=COLORS["card"])
        checks_frame.pack(fill="x", **pad, pady=(0, 8))
        self.check_widgets = {}
        for key, label in CHECKS:
            fr = tk.Frame(checks_frame, bg=COLORS["card"])
            fr.pack(fill="x", pady=3)
            dot = tk.Label(fr, text="–", width=2,
                           font=("Segoe UI", 11, "bold"),
                           fg=COLORS["check_off_fg"],
                           bg=COLORS["check_off_bg"])
            dot.pack(side="left", ipadx=3, ipady=1)
            lbl = tk.Label(fr, text=label, font=("Segoe UI", 11),
                           fg=COLORS["muted"], bg=COLORS["card"])
            lbl.pack(side="left", padx=8)
            self.check_widgets[key] = (dot, lbl)

        # Tip box
        self.tip_frame = tk.Frame(card, bg=COLORS["tip_bg"],
                                  highlightbackground="#fde68a",
                                  highlightthickness=1)
        self.tip_lbl = tk.Label(self.tip_frame, text="",
                                font=("Segoe UI", 10),
                                fg=COLORS["tip_fg"],
                                bg=COLORS["tip_bg"],
                                wraplength=360, justify="left")
        self.tip_lbl.pack(padx=10, pady=7)

        self._sep(card)

        # Entropy section
        ent_frame = tk.Frame(card, bg=COLORS["card"])
        ent_frame.pack(fill="x", **pad, pady=(0, 20))
        self._stat_row(ent_frame, "Entropy estimate", "entropy_val")
        self._stat_row(ent_frame, "Character pool size", "pool_val")

        self.entry.focus()

    def _stat_row(self, parent, label, attr):
        fr = tk.Frame(parent, bg=COLORS["card"])
        fr.pack(fill="x", pady=2)
        tk.Label(fr, text=label, font=("Segoe UI", 11),
                 fg=COLORS["muted"], bg=COLORS["card"]).pack(side="left")
        lbl = tk.Label(fr, text="—", font=("Courier New", 11, "bold"),
                       fg=COLORS["text"], bg=COLORS["card"])
        lbl.pack(side="right")
        setattr(self, attr, lbl)

    def _sep(self, parent):
        tk.Frame(parent, bg=COLORS["border"], height=1).pack(
            fill="x", padx=24, pady=8)

    # ── Interaction ───────────────────────────────────────────────────────────

    def _toggle_pw(self):
        self._show_pw = not self._show_pw
        self.entry.config(show="" if self._show_pw else "•")
        self.eye_btn.config(text="🔒" if self._show_pw else "👁")

    def _on_change(self):
        pw = self.pw_var.get()
        result = analyse(pw)
        if result is None:
            self._reset()
            return
        self._update(pw, result)

    # ── Rendering ─────────────────────────────────────────────────────────────

    def _reset(self):
        bar_color_map = {1: COLORS["bar_empty"], 2: COLORS["bar_empty"],
                         3: COLORS["bar_empty"], 4: COLORS["bar_empty"],
                         5: COLORS["bar_empty"]}
        for i, b in enumerate(self.bars):
            b.config(bg=COLORS["bar_empty"])

        self.strength_lbl.config(text="—", fg=COLORS["muted"])
        self.score_lbl.config(text="")
        self.leaked_frame.pack_forget()
        self.tip_frame.pack_forget()

        for key, _ in CHECKS:
            dot, lbl = self.check_widgets[key]
            dot.config(text="–", fg=COLORS["check_off_fg"],
                       bg=COLORS["check_off_bg"])
            lbl.config(fg=COLORS["muted"])

        self.entropy_val.config(text="—")
        self.pool_val.config(text="—")

    def _update(self, pw, r):
        score  = r["score"]
        leaked = r["leaked"]

        # Bar colors
        score_color = (COLORS["weak"] if score <= 2
                       else COLORS["medium"] if score == 3
                       else COLORS["strong"])
        for i, b in enumerate(self.bars):
            b.config(bg=score_color if i < score else COLORS["bar_empty"])

        # Strength label
        labels = {0:"—", 1:"Weak", 2:"Weak", 3:"Medium", 4:"Strong", 5:"Very strong"}
        if leaked:
            self.strength_lbl.config(text="Leaked — change it",
                                     fg=COLORS["weak"])
        else:
            self.strength_lbl.config(text=labels[score], fg=score_color)
        self.score_lbl.config(text=f"{score}/5")

        # Leaked banner
        if leaked:
            self.leaked_frame.pack(fill="x", padx=24, pady=(0, 6))
        else:
            self.leaked_frame.pack_forget()

        # Check rows
        for key, _ in CHECKS:
            dot, lbl = self.check_widgets[key]
            passed = r["checks"][key]
            if passed:
                dot.config(text="✓", fg=COLORS["check_ok_fg"],
                           bg=COLORS["check_ok_bg"])
                lbl.config(fg=COLORS["text"])
            else:
                dot.config(text="✗", fg=COLORS["check_bad_fg"],
                           bg=COLORS["check_bad_bg"])
                lbl.config(fg=COLORS["muted"])

        # Tip box
        if r["tip"]:
            self.tip_lbl.config(text="💡  " + r["tip"])
            self.tip_frame.pack(fill="x", padx=24, pady=(0, 6))
        else:
            self.tip_frame.pack_forget()

        # Entropy
        self.entropy_val.config(text=f"{r['entropy']} bits")
        self.pool_val.config(text=f"{r['pool']} chars")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = PasswordApp()
    app.mainloop()