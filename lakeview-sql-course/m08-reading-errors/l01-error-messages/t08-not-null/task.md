This statement:

```sql
INSERT INTO users (name, password_hash) VALUES ('Maria', 'demo-hash');
```

gave this error:

```text
NOT NULL constraint failed: users.email
```

What is the fix?
