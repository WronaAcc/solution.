# solution.py
import re
import pandas as pd

LABEL_RE = re.compile(r"^[A-Za-z_]+$")
TOKEN_RE = re.compile(r"[A-Za-z_]+|[+\-*]")

def add_virtual_column(df, role, new_column):
    if not isinstance(df, pd.DataFrame):
        return pd.DataFrame([])

    if any(not LABEL_RE.fullmatch(str(c)) for c in df.columns):
        return pd.DataFrame([])

    if not isinstance(new_column, str) or not LABEL_RE.fullmatch(new_column):
        return pd.DataFrame([])

    if not isinstance(role, str):
        return pd.DataFrame([])
    expr = role.strip()
    if not expr:
        return pd.DataFrame([])

    tokens = TOKEN_RE.findall(expr)
    if "".join(tokens) != re.sub(r"\s+", "", expr):
        return pd.DataFrame([])

    if len(tokens) % 2 == 0:
        return pd.DataFrame([])

    for i, t in enumerate(tokens):
        if i % 2 == 0:
            if not LABEL_RE.fullmatch(t) or t not in df.columns:
                return pd.DataFrame([])
        else:
            if t not in {"+", "-", "*"}:
                return pd.DataFrame([])

    values = [df[tokens[i]] for i in range(0, len(tokens), 2)]
    ops    = [tokens[i] for i in range(1, len(tokens), 2)]

    i = 0
    while i < len(ops):
        if ops[i] == "*":
            values[i] = values[i] * values[i + 1]
            del values[i + 1]
            del ops[i]
        else:
            i += 1

    result = values[0]
    for i, op in enumerate(ops, start=1):
        result = result + values[i] if op == "+" else result - values[i]

    out = df.copy()
    out[new_column] = result
    return out