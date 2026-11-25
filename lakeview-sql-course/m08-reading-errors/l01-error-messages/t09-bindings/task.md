This Python line:

```python
conn.execute("SELECT * FROM users WHERE email = ?", (email))
```

gave this error when `email` was `'mary@example.com'`:

```text
sqlite3.ProgrammingError: Incorrect number of bindings supplied. The current statement uses 1, and there are 16 supplied.
```

What is the fix?
