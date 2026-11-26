# SQL with SQLite - The Lakeview Hotel

A JetBrains Academy course for practising SQL with SQLite. All 76 tasks use
one small database for the Lakeview Hotel, and hidden tests check each answer
inside PyCharm.

## Taking the course

Install the JetBrains Academy plugin in PyCharm, then find SQL with SQLite - The
Lakeview Hotel in the course catalogue. You can also open a course archive (a `.zip` made by
the plugin) from the plugin's start screen.

## What it covers

1. Reading data: SELECT, WHERE, ORDER BY, LIKE, and NULL
2. Creating tables: types, keys, constraints, and foreign keys
3. Changing data: INSERT, UPDATE, DELETE, and transactions
4. Counting and grouping: aggregates, GROUP BY, and HAVING
5. Joining tables: inner joins, LEFT JOIN, and joins across four tables
6. Dates and subqueries: julianday, clash checks, and NOT EXISTS
7. SQL from Python: the sqlite3 module, placeholders, and IntegrityError
8. Reading errors: what SQLite error messages mean

## Repository layout

| Folder | What it holds |
|---|---|
| `lakeview-sql-course/` | The course itself. Open this folder in PyCharm to edit, archive, or upload it. |
| `generator/` | The Python scripts that write `lakeview-sql-course/`. Change the course here, not by hand. |

To change a task, edit its module file in `generator/`, then run:

```
python generator/build.py
python generator/validate.py
```

`build.py` rewrites the course folder. It keeps the plugin's
`*-remote-info.yaml` files, which hold the Marketplace ids, so commit those
files too. See `generator/README.md` for more.

## Licence

| What | Licence |
|---|---|
| Code: every `.py` and `.sql` file, including the generator, `run.py`, the hidden tests, and `lakeview.sql` | [GPL-3.0-or-later](LICENSES/GPL-3.0-or-later.txt) |
| Teaching content: task text, READMEs, and quiz text | [CC-BY-SA-4.0](LICENSES/CC-BY-SA-4.0.txt) |

See `LICENSE` for the details. `REUSE.toml` records the same split in
machine-readable form, following the [REUSE](https://reuse.software)
specification.
