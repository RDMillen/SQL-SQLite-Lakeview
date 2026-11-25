This statement:

```sql
INSERT INTO users (name, email, password_hash) VALUES ('James', 'james@example.com', 'demo-hash');
```

gave this error:

```text
UNIQUE constraint failed: users.email
```

What is the fix?
