# Virtual Column Task

This repository implements a simple helper to add a **virtual column** to a pandas `DataFrame` based on a basic arithmetic expression.

## What’s included
- `solution.py` — straightforward, single-function implementation (the primary solution).
- `test_virtual_column 1.py` — tests provided with the task.
- `second_solution.py` — optional refactor with small helper functions and a class (`VirtualColumnAdder`).  
  It **keeps** a `add_virtual_column` function so tests can still import it the same way.

## Function
```python
add_virtual_column(df, role, new_column) -> pandas.DataFrame
```
## Rules
- Allowed operators in `role`: `+`, `-`, `*`
- Column labels and `new_column`: letters and underscore only (`^[A-Za-z_]+$`)
- `role` may contain spaces (e.g. `"a + b * c"`)
- On any validation/parsing error: return an empty `DataFrame`
- The input `df` must not be modified (work on a copy)
  
## Example
```python
import pandas as pd
from solution import add_virtual_column

df = pd.DataFrame({
  "quantity": [10, 3],
  "price":    [10, 1],
  "name":     ["banana", "apple"]
})

out = add_virtual_column(df[["quantity", "price"]], "quantity * price", "total")
print(out)
# -> adds a new 'total' column with [100, 3]
```
## Tests
Run either:
```bash
python "test_virtual_column 1.py"
# or
pytest -q
```
## Optional OOP version
The refactored version is in `second_solution.py`:
- `add_virtual_column(df, role, new_column) - same function signature (compatible with tests)
- `VirtualColumnAdder(df).add(role, new_column) - simple class API
## Example:
```python
from second_solution import add_virtual_column
# or:
from second_solution import VirtualColumnAdder
out = VirtualColumnAdder(df).add("a + b * c", "res")
```
