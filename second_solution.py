import re
import pandas as pd

LABEL_RE = re.compile(r"^[A-Za-z_]+$")
TOKEN_RE = re.compile(r"[A-Za-z_]+|[+\-*]")

def _is_valid_df(df: pd.DataFrame) -> bool:
    return isinstance(df, pd.DataFrame) and all(LABEL_RE.fullmatch(str(c)) for c in df.columns)

def _is_valid_name(name: str) -> bool:
    return isinstance(name, str) and LABEL_RE.fullmatch(name) is not None

def _tokenize(expr: str):
    if not isinstance(expr, str):
        return None
    expr = expr.strip()
    if not expr:
        return None
    tokens = TOKEN_RE.findall(expr)
    if "".join(tokens) != re.sub(r"\s+", "", expr):
        return None
    return tokens

def _validate_tokens(tokens, df: pd.DataFrame) -> bool:
    if not tokens or len(tokens) % 2 == 0:
        return False
    for i, t in enumerate(tokens):
        if i % 2 == 0:
            if not LABEL_RE.fullmatch(t) or t not in df.columns:
                return False
        else:
            if t not in {"+", "-", "*"}:
                return False
    return True

def _evaluate(tokens, df: pd.DataFrame) -> pd.Series:
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
    return result

class VirtualColumnAdder:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def add(self, role: str, new_column: str) -> pd.DataFrame:
        if not _is_valid_df(self.df) or not _is_valid_name(new_column):
            return pd.DataFrame([])
        tokens = _tokenize(role)
        if tokens is None or not _validate_tokens(tokens, self.df):
            return pd.DataFrame([])
        try:
            result = _evaluate(tokens, self.df)
        except Exception:
            return pd.DataFrame([])
        out = self.df.copy()
        out[new_column] = result
        return out

def add_virtual_column(df: pd.DataFrame, role: str, new_column: str) -> pd.DataFrame:
    return VirtualColumnAdder(df).add(role, new_column)