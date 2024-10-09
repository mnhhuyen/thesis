import duckdb

con = duckdb.connect(database='/media/data/huyennm/mimic-iv/mimic-derived/derived_database/derived.db')
tables = con.execute("SHOW TABLES;").fetchall()
print(tables)

